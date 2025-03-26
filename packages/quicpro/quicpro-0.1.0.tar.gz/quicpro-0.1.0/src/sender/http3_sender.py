import logging
from typing import Any
from quicpro.exceptions import TransmissionError

logger = logging.getLogger(__name__)

class HTTP3Sender:
    """
    Maps the encoded frame onto an HTTP/3 stream.
    """
    def __init__(self, quic_sender: Any, stream_id: int) -> None:
        """
        Initialize the HTTP3Sender with a QUIC sender and an HTTP/3 stream identifier.

        Args:
            quic_sender (Any): An instance responsible for sending QUIC packets.
            stream_id (int): The identifier for the HTTP/3 stream.
        """
        self.quic_sender = quic_sender
        self.stream_id = stream_id

    def send(self, frame: bytes) -> None:
        """
        Maps the encoded frame to an HTTP/3 stream frame and sends it using the QUIC sender.

        Args:
            frame (bytes): The encoded frame to map onto the HTTP/3 stream.

        Raises:
            TransmissionError: If mapping or transmission of the frame fails.
        """
        try:
            stream_frame = b"HTTP3Stream(stream_id=%d, payload=" % self.stream_id + frame + b")"
            logger.info("HTTP3Sender created stream frame: %s", stream_frame)
            self.quic_sender.send(stream_frame)
        except Exception as e:
            logger.exception("HTTP3Sender mapping failed: %s", e)
            raise TransmissionError(f"HTTP3Sender failed to send stream frame: {e}") from e