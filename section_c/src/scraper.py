import os
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
def setup_logger():
    # Get base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(base_dir, "data", "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Create a logger
    logger = logging.getLogger('yahoo_finance_scraper')
    logger.setLevel(logging.DEBUG)

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s\n'
        'File: %(filename)s - Function: %(funcName)s - Line: %(lineno)d\n'
        '-------------------------------------------------------------------'
    )
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')

    # Create and configure file handler with rotation
    log_file = os.path.join(log_dir, "scraper.log")
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)

    # Create and configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger, base_dir 