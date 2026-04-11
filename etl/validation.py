"""
Validation module for ETL data quality checks.

This module provides functions to validate the integrity and quality
of data during the ETL process.
"""

from etl.logger import get_logger

logger = get_logger()
def validate(df):
    try:
        assert df.shape[0] > 0, "Empty dataset"
        logger.info("Validation completed successfully.")
        return True
    except AssertionError as e:
        logger.error(f"Validation failed: {e}")
        return False
    