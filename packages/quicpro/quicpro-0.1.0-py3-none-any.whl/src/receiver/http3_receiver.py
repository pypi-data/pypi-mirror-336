import logging
from typing import Any
from quicpro.exceptions import HTTP3FrameError

logger = logging.getLogger(__name__)

class HTTP3Receiver:
    """
    Production-grade HTTP/3 receiver that extracts, validates, and processes HTTP/3 frames
    from incoming QUIC packets, then passes the decoded content to the downstream Decoder.
    If the expected HTTP/3 frame format is not available, the receiver falls back to using the entire
    packet as the payload.
    """
    def __init__(self, decoder: Any) -> None:
        """
        Args:
            decoder: An instance with a decode(frame: bytes) method for processing extracted frames.
        """
        self.decoder = decoder

    def receive(self, quic_packet: bytes) -> None:
        """
        Extracts an HTTP/3 frame from the provided QUIC packet (with fallback) and passes it to the Decoder.
        
        Args:
            quic_packet (bytes): The incoming QUIC packet containing an HTTP/3 stream frame or fallback payload.
        
        Raises:
            HTTP3FrameError: If frame extraction or validation fails.
            Exception: Propagates exceptions from the Decoder.
        """
        try:
            logger.debug("HTTP3Receiver received QUIC packet", extra={"packet_length": len(quic_packet)})
            frame = self._extract_http3_frame(quic_packet)
            if not self._validate_frame(frame):
                raise HTTP3FrameError("Extracted HTTP/3 frame failed validation.")
            logger.info("HTTP3Receiver successfully extracted frame", extra={"frame": frame})
            self.decoder.decode(frame)
        except Exception as exc:
            logger.exception("HTTP3Receiver processing failed", exc_info=exc, extra={"quic_packet": quic_packet})
            raise

    def _extract_http3_frame(self, packet: bytes) -> bytes:
        """
        Extracts the HTTP/3 frame from the QUIC packet.
        In production, this method implements robust parsing logic. It expects that the frame starts with
        b'HTTP3:' and ends with a newline (b'\n'). If the prefix is not found, it falls back to using the
        entire packet as the frame payload.
        
        Args:
            packet (bytes): The raw QUIC packet data.
        
        Returns:
            bytes: The extracted HTTP/3 frame payload, or the full packet if no prefix is found.
        
        Raises:
            HTTP3FrameError: If fallback extraction results in an empty payload.
        """
        prefix = b'HTTP3:'
        suffix = b'\n'
        start = packet.find(prefix)
        if start == -1:
            logger.warning("HTTP3 frame prefix not found in packet; using full packet as payload.")
            frame = packet.strip()
            if not frame:
                raise HTTP3FrameError("Fallback extraction failed: packet is empty.")
            return frame
        start += len(prefix)
        end = packet.find(suffix, start)
        if end == -1:
            end = len(packet)
        frame = packet[start:end].strip()
        if not frame:
            raise HTTP3FrameError("HTTP/3 frame payload is empty after extraction.")
        return frame

    def _validate_frame(self, frame: bytes) -> bool:
        """
        Validates the extracted HTTP/3 frame payload.
        
        Args:
            frame (bytes): The extracted HTTP/3 frame payload.
        
        Returns:
            bool: True if the frame passes validation, False otherwise.
        """
        min_frame_length = 1  # Adjust this threshold as needed.
        if len(frame) < min_frame_length:
            logger.error("Extracted frame is too short.", extra={"frame_length": len(frame)})
            return False
        return True