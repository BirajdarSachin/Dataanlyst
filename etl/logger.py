import logging

def get_logger():
    """
    Returns a configured logger for ETL processes.
    The logger writes to 'ETL.log' with INFO level and above.
    """
    logger = logging.getLogger("etl_logger")
    logger.setLevel(logging.INFO)

    # Remove old handlers (important in notebooks / reruns)
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler("logs/ETL.log")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


