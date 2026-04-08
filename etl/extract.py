import pandas as pd
from etl.logger import get_logger

logger = get_logger()

def extract_data(file_path):
    """
    Extract data from a CSV file.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the extracted data.
    """
    try:
        data = pd.read_csv(file_path)
        logger.info(f"Data successfully extracted from {file_path}")
        logger.info(f"Extracted {len(data)} rows from source '{file_path}' ")
        return data
    except Exception as e:
        logger.error(f"An error occurred while extracting data: {e}")
        return None