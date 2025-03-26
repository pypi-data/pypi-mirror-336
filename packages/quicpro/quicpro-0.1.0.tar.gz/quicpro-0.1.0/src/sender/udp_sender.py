import logging
import time
from typing import Any
from quicpro.exceptions import TransmissionError

logger = logging.getLogger(__name__)

class UDPSender:
    """
    Production-ready UDPSender for transmitting encrypted packets over UDP.
    This class wraps a network abstraction (which must provide a `transmit` method)
    and enhances it with retry logic, context management, and structured logging.

    Attributes:
        network: An instance providing a `transmit(encrypted_packet: bytes) -> int` method.
        max_retries: The maximum number of retries for transient failures.
        retry_delay: Base delay (in seconds) between retries; delay increases with each attempt.
    """
    def __init__(self, network: Any, max_retries: int = 3, retry_delay: float = 0.5) -> None:
        """
        Initialize the UDPSender.

        Args:
            network: A network instance with a `transmit` method.
            max_retries: Maximum number of retry attempts (default is 3).
            retry_delay: Base delay between retries in seconds (default is 0.5).
        """
        self.network = network
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def send(self, encrypted_packet: bytes) -> int:
        """
        Send an encrypted packet over UDP.
        This method attempts to send the packet and retries on failure.

        Args:
            encrypted_packet (bytes): The data packet to transmit.

        Returns:
            int: The number of bytes sent.

        Raises:
            TransmissionError: If all retry attempts fail.
        """
        attempt = 0
        while attempt <= self.max_retries:
            try:
                bytes_sent = self.network.transmit(encrypted_packet)
                logger.info("UDPSender sent %d bytes on attempt %d", bytes_sent, attempt + 1)
                return bytes_sent
            except Exception as e:
                attempt += 1
                logger.exception("UDPSender failed on attempt %d: %s", attempt, e)
                if attempt > self.max_retries:
                    raise TransmissionError(
                        f"Failed to send packet after {self.max_retries} attempts: {e}"
                    ) from e
                time.sleep(self.retry_delay * attempt)
        raise RuntimeError("Reached unexpected end of UDPSender.send()")

    def __enter__(self) -> "UDPSender":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # Close underlying network resources if available.
        if hasattr(self.network, "close"):
            try:
                self.network.close()
                logger.info("Network resources closed successfully.")
            except Exception as e:
                logger.exception("Error closing network resources: %s", e)