import logging
import os
from datetime import datetime
from google.cloud.logging.handlers import CloudLoggingHandler
from .client import get_client

def create_instance(base_dir:str, service_name:str, category:str) -> logging.Logger:
    """
    Initializes and returns the requested logger.

    - Logs are stored in `base_dir/logs/{type}`
    - Uses Google Cloud Logging if configured

    Args:
        base_dir (str): The base directory where logs should be stored (e.g., "/path/to/maleo_security")
        service_name (str): The name of the service (e.g., "maleo_security")
        category (str): The logger category (e.g., "application" or "middleware")

    Returns:
        logging.Logger: Configured logger instance
    """
    #* Define logger name
    logger_name = f"{service_name} - {category}"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    #* Prevent duplicate handlers
    if logger.hasHandlers():
        return logger

    #* Configure formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    #* Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    #* Google Cloud Logging handler (If enabled)
    try:
        client = get_client()
        cloud_handler = CloudLoggingHandler(client.client, name=logger_name.replace(" ", ""))
        logger.addHandler(cloud_handler)
    except Exception as e:
        logger.warning(f"Failed to initialize Google Cloud Logging: {str(e)}")

    #* Define log directory at project root (e.g., `maleo_service/logs/{category}`)
    log_dir = os.path.join(base_dir, f"logs/{category}")
    os.makedirs(log_dir, exist_ok=True)

    #* Generate a timetamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = os.path.join(log_dir, f"{timestamp}.log")

    #* File handler
    file_handler = logging.FileHandler(log_filename, mode="a")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger