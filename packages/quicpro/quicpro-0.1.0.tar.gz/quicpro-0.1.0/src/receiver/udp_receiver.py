import socket
import selectors
import threading
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Tuple, Optional, Any

logger = logging.getLogger(__name__)

class UDPReceiver:
    """
    A production-grade UDPReceiver that listens on a specified bind_address,
    receives UDP packets using nonblocking I/O (selectors), processes them concurrently,
    and automatically attempts to rebind the socket on unrecoverable errors.
    Supports backward compatibility by accepting either a 'packet_handler'
    or a 'tls_decryptor'. If 'tls_decryptor' is provided without a packet_handler,
    a default handler is created to call tls_decryptor.decrypt(data). Additionally,
    if tls_decryptor is provided, it is stored as an attribute.
    """
    def __init__(
        self,
        bind_address: Tuple[str, int],
        tls_decryptor: Optional[Any] = None,
        packet_handler: Optional[Callable[[bytes, Tuple[str, int]], None]] = None,
        buffer_size: int = 4096,
        max_rebind_attempts: int = 3,
        rebind_backoff: float = 1.0,
        max_workers: int = 8,
    ) -> None:
        self.bind_address = bind_address
        self.buffer_size = buffer_size
        self.max_rebind_attempts = max_rebind_attempts
        self.rebind_backoff = rebind_backoff
        self.selector = selectors.DefaultSelector()
        self.socket: Optional[socket.socket] = None
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._lock = threading.Lock()
        self.tls_decryptor = tls_decryptor
        if packet_handler is None and tls_decryptor is not None:
            self.packet_handler = lambda data, addr: tls_decryptor.decrypt(data)
        elif packet_handler is not None:
            self.packet_handler = packet_handler
        else:
            raise ValueError("Either 'packet_handler' or 'tls_decryptor' must be provided.")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def _create_and_bind_socket(self) -> None:
        if self.socket:
            self._cleanup_socket()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setblocking(False)
        try:
            s.bind(self.bind_address)
        except Exception as e:
            s.close()
            raise e
        self.socket = s
        self.selector.register(self.socket, selectors.EVENT_READ)
        logger.info("Socket bound to %s", self.bind_address)

    def start(self) -> None:
        with self._lock:
            if self.running:
                logger.warning("UDPReceiver is already running.")
                return
            self.running = True
            self._create_and_bind_socket()
            self._thread = threading.Thread(target=self._event_loop, daemon=True)
            self._thread.start()
            logger.info("UDPReceiver started.")

    def _event_loop(self) -> None:
        rebind_attempts = 0
        while self.running:
            try:
                events = self.selector.select(timeout=1)
                for key, mask in events:
                    if mask & selectors.EVENT_READ:
                        try:
                            data, addr = self.socket.recvfrom(self.buffer_size)
                        except BlockingIOError:
                            continue
                        except Exception as e:
                            logger.exception("Error receiving data: %s", e)
                            raise
                        self.executor.submit(self._handle_packet, data, addr)
            except Exception as e:
                logger.exception("Event loop encountered error: %s", e)
                rebind_attempts += 1
                if rebind_attempts > self.max_rebind_attempts:
                    logger.error("Max rebind attempts exceeded; stopping UDPReceiver.")
                    self.stop()
                else:
                    logger.info("Rebinding socket (attempt %d)", rebind_attempts)
                    time.sleep(self.rebind_backoff * rebind_attempts)
                    try:
                        self._create_and_bind_socket()
                        rebind_attempts = 0
                    except Exception as bind_error:
                        logger.exception("Failed to rebind socket: %s", bind_error)
            time.sleep(0.01)
        logger.info("Event loop terminated.")

    def _handle_packet(self, data: bytes, addr: Tuple[str, int]) -> None:
        try:
            self.packet_handler(data, addr)
        except Exception as e:
            logger.exception("Packet handler error for %s: %s", addr, e)

    def _cleanup_socket(self) -> None:
        if self.socket:
            try:
                self.selector.unregister(self.socket)
            except Exception as e:
                logger.debug("Error unregistering socket: %s", e)
            try:
                self.socket.close()
            except Exception as e:
                logger.debug("Error closing socket: %s", e)
            self.socket = None

    def stop(self) -> None:
        with self._lock:
            if not self.running:
                return
            self.running = False
            self._cleanup_socket()
        if self._thread:
            self._thread.join(timeout=5)
        self.executor.shutdown(wait=True)
        logger.info("UDPReceiver stopped gracefully.")