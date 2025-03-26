import logging
from typing import Optional, Callable

from pydantic import BaseModel, Field
from quicpro.exceptions import PipelineError

logger = logging.getLogger(__name__)


class ConsumerConfig(BaseModel):
    """
    Configuration model for the ConsumerApp.

    Attributes:
        process_callback (Optional[Callable[[str], None]]): 
            An optional callback function for additional message processing.
    """
    process_callback: Optional[Callable[[str], None]] = Field(default=None)


class ConsumerApp:
    """
    Production-ready ConsumerApp for processing final decoded messages.

    This implementation logs structured information about incoming messages
    and supports an optional callback for extended processing.
    """
    def __init__(self, config: Optional[ConsumerConfig] = None) -> None:
        """
        Initialize the ConsumerApp with an optional configuration.

        Args:
            config (Optional[ConsumerConfig]): Configuration settings for ConsumerApp.
        """
        if config is None:
            config = ConsumerConfig()
        self.process_callback = config.process_callback

    def consume(self, message: str) -> None:
        """
        Consume a final decoded message.

        Logs the received message and, if a process callback is provided, calls it.

        Args:
            message (str): The decoded message to process.

        Raises:
            PipelineError: If an exception occurs during message processing.
        """
        try:
            logger.info("ConsumerApp received message", extra={"message": message})
            if self.process_callback:
                self.process_callback(message)
        except Exception as exc:
            logger.exception("ConsumerApp processing failed", exc_info=exc)
            raise PipelineError(f"ConsumerApp failed to process message: {exc}") from exc