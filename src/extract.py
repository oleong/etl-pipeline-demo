"""
extract.py — Stage 1: Data Extraction
======================================
Loads raw CSV data from the /data/raw directory.

In a real deployment this module would connect to an API,
a database, or a message broker (Kafka). For this demo we
use a local CSV to keep the focus on pipeline structure.

Author  : Oscar León
Dataset : UCI Heart Disease Dataset (Cleveland, 1988)
"""

import os
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def load_csv(filepath: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a raw DataFrame.

    Parameters
    ----------
    filepath : str
        Absolute or relative path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Raw, unmodified data as loaded from disk.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at the given path.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    df = pd.read_csv(filepath)
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns from {filepath}")
    return df


if __name__ == "__main__":
    # Quick smoke-test when running this module directly
    df = load_csv("data/raw/heart.csv")
    print(df.head())
    print(df.dtypes)
