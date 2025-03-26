from typing import Union
from quicpro.sender.encoder import Encoder, Message

class ProducerApp:
    def __init__(self, encoder: Encoder) -> None:
        self.encoder = encoder

    def create_message(self, message: Union[str, Message, dict]) -> None:
        """
        Accepts a message as a string, dict, or Message instance and sends it through the encoder.
        """
        if isinstance(message, Message):
            msg_obj = message
        elif isinstance(message, dict):
            msg_obj = Message(**message)
        else:
            msg_obj = Message(content=message)
        self.encoder.encode(msg_obj)