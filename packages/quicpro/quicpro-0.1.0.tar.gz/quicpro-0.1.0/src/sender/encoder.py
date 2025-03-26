import logging
from typing import Any
from pydantic import BaseModel
from quicpro.exceptions import EncodingError

logger = logging.getLogger(__name__)


class Message(BaseModel):
    content: str


class Encoder:
    """
    Encodes a message into a binary frame using a validated Pydantic model.
    """
    def __init__(self, http3_sender: Any) -> None:
        self.http3_sender = http3_sender

    def encode(self, message: Message) -> None:
        try:
            encoded_frame = f"Frame({message.content})".encode("utf-8")
            logger.info("Encoder produced frame: %s", encoded_frame)
            self.http3_sender.send(encoded_frame)
        except Exception as e:
            logger.exception("Encoding failed: %s", e)
            raise EncodingError(f"Encoding failed: {e}") from e