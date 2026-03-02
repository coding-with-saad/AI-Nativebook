import logging
import os

def setup_logger(name: str = "rag_agent", level: str = "INFO") -> logging.Logger:
    """
    Sets up a logger with a specified name and level.

    Args:
        name: The name of the logger.
        level: The logging level (e.g., "INFO", "DEBUG", "WARNING").

    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        # If logger already has handlers, it means it was already configured
        return logger

    # Set logging level from environment variable or default to INFO
    log_level = os.getenv("LOG_LEVEL", level).upper()
    logger.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create console handler and set level
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

# Example usage (can be removed or modified in production)
if __name__ == "__main__":
    app_logger = setup_logger()
    app_logger.info("This is an informational message.")
    app_logger.debug("This is a debug message.") # Won't show if level is INFO
    app_logger.warning("This is a warning message.")

    os.environ["LOG_LEVEL"] = "DEBUG"
    debug_logger = setup_logger("debug_app")
    debug_logger.debug("This debug message will show.")
