"""
Logging module for Kagan Collection Management Software
Provides comprehensive logging for debugging and error tracking
"""
import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# Create log file with timestamp
log_filename = os.path.join(LOGS_DIR, f'kagan_{datetime.now().strftime("%Y%m%d")}.log')

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()  # Also print to console
    ]
)

# Create logger for the application
logger = logging.getLogger('KaganApp')

def log_exception(context, exception):
    """Log an exception with context information"""
    logger.error(f"{context}: {type(exception).__name__}: {str(exception)}", exc_info=True)

def log_info(message):
    """Log an informational message"""
    logger.info(message)

def log_warning(message):
    """Log a warning message"""
    logger.warning(message)

def log_error(message):
    """Log an error message"""
    logger.error(message)

def log_debug(message):
    """Log a debug message"""
    logger.debug(message)
