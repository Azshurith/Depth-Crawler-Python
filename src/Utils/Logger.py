import logging
import os
from datetime import datetime

# Capture runtime timestamp once when the application starts
RUNTIME_TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

def Logger(name: str, log_dir: str = "logs", log_file: str = "runtime.log") -> logging.Logger:
    """
    Creates and returns a logger instance with logs stored in a runtime-timestamped directory.

    :param name: Name of the logger.
    :param log_dir: Directory where logs will be stored.
    :param log_file: Name of the log file.
    :return: Configured logger instance.
    """
    # Create a runtime-timestamped directory
    log_path = os.path.join(log_dir, RUNTIME_TIMESTAMP)

    # Ensure the log directory exists
    os.makedirs(log_path, exist_ok=True)

    # Full path to the log file
    log_file_path = os.path.join(log_path, log_file)

    # Set up the logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)

    # Set formatter for both handlers
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] (%(name)s): %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Avoid adding multiple handlers in case of repeated calls
    logger.propagate = False

    return logger
