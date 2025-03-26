import logging
from typing import Any
from quicpro.exceptions import DecodingError

logger = logging.getLogger(__name__)

class Decoder:
    """
    Production-ready Decoder that extracts message content from an HTTP/3 frame.
    The expected format is "Frame(content)". If the pattern isn't found, the content defaults to "Unknown".
    Once extracted, the message is passed to the provided consumer_app.
    """
    def __init__(self, consumer_app: Any) -> None:
        """
        Args:
            consumer_app: An object with a consume(message: str) method to process the decoded message.
        """
        self.consumer_app = consumer_app

    def decode(self, quic_packet: bytes) -> None:
        """
        Decode the provided QUIC packet to extract the original message content.
        Expected packet format: Contains "Frame(content)". If the pattern is not found,
        defaults the message to "Unknown".

        Args:
            quic_packet (bytes): The raw packet data to decode.
        
        Raises:
            DecodingError: If an error occurs during decoding.
        """
        try:
            frame_prefix = b"Frame("
            start_index = quic_packet.find(frame_prefix)
            if start_index != -1:
                start_index += len(frame_prefix)
                end_index = quic_packet.find(b")", start_index)
                if end_index != -1:
                    message_content = quic_packet[start_index:end_index].decode("utf-8")
                else:
                    logger.warning("Decoder: Closing delimiter not found; defaulting message to 'Unknown'.")
                    message_content = "Unknown"
            else:
                logger.warning("Decoder: Frame prefix not found; defaulting message to 'Unknown'.")
                message_content = "Unknown"
            logger.info("Decoder extracted message: %s", message_content)
            self.consumer_app.consume(message_content)
        except Exception as exc:
            logger.exception("Decoder encountered an error while processing packet: %s", exc)
            raise DecodingError(f"Error decoding quic packet: {exc}") from exc