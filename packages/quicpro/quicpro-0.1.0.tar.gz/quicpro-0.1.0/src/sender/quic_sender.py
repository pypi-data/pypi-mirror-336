import logging
import hashlib
from typing import Any
from quicpro.exceptions import TransmissionError

logger = logging.getLogger(__name__)

class QUICSender:
    """
    Production-grade QUICSender that packages HTTP/3 stream frames into structured QUIC packets.
    Packet Structure:
      - Header Marker: b'QUIC' (4 bytes)
      - Payload Length: 4-byte big-endian integer representing the length of the stream frame.
      - Checksum: 8-byte truncated SHA256 digest of the stream frame.
      - Payload: The HTTP/3 stream frame.
    The resulting packet is then passed to the TLS encryptor for further processing.
    """
    def __init__(self, tls_encryptor: Any) -> None:
        """
        Initialize the QUICSender with a TLS encryptor instance.

        Args:
            tls_encryptor: An object providing an encrypt(packet: bytes) method.
        """
        self.tls_encryptor = tls_encryptor

    def send(self, stream_frame: bytes) -> None:
        """
        Package the HTTP/3 stream frame into a QUIC packet and pass it to the TLS encryptor.

        Args:
            stream_frame (bytes): The HTTP/3 stream frame to be sent.

        Raises:
            TransmissionError: If an error occurs during packet construction or encryption.
        """
        try:
            header_marker = b'QUIC'
            frame_length = len(stream_frame)
            length_bytes = frame_length.to_bytes(4, byteorder='big')
            checksum = hashlib.sha256(stream_frame).digest()[:8]
            quic_packet = header_marker + length_bytes + checksum + stream_frame
            logger.info("QUICSender packaged packet: %s", quic_packet)
            self.tls_encryptor.encrypt(quic_packet)
        except Exception as e:
            logger.exception("QUICSender packaging failed: %s", e)
            raise TransmissionError(f"QUICSender failed to package and send packet: {e}") from e