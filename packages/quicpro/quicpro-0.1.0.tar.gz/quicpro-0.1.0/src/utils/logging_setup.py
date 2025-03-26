import logging
import sys

def setup_logging(level=logging.INFO):
    """
    Configures root logging for the application.

    :param level: The logging level to use (e.g., logging.INFO).
    """
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Clear existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    logging.info("Logging is configured with level %s", logging.getLevelName(level))