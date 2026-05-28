"""
load.py — Stage 3: Data Loading
=================================
Writes the cleaned DataFrame to two destinations:
  1. A PostgreSQL table (primary destination, via SQLAlchemy)
  2. A CSV file in data/processed/ (backup / audit trail)

Environment variables (set in .env or docker-compose.yml):
  DB_HOST     — PostgreSQL hostname  (default: localhost)
  DB_PORT     — PostgreSQL port      (default: 5432)
  DB_NAME     — Database name        (default: etl_demo)
  DB_USER     — Username             (default: etl_user)
  DB_PASSWORD — Password             (required)

Author  : Oscar León
"""

import os
import logging
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)


def _get_db_url() -> str:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "etl_demo")
    user = os.getenv("DB_USER", "etl_user")
    password = os.getenv("DB_PASSWORD", "")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


def load_to_postgres(df: pd.DataFrame, table_name: str = "heart_disease") -> None:
    """
    Writes the DataFrame to a PostgreSQL table.

    Uses 'replace' strategy on each run so the demo stays idempotent
    (safe to run multiple times without duplicating rows).
    In production you would likely use 'append' with deduplication logic.

    Parameters
    ----------
    df : pd.DataFrame
        Transformed DataFrame.
    table_name : str
        Target table name. Created automatically if it does not exist.
    """
    url = _get_db_url()
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # verify connection

        df.to_sql(table_name, engine, if_exists="replace", index=False)
        logger.info(f"Loaded {len(df)} rows into table '{table_name}'.")

    except OperationalError as e:
        logger.error(f"Could not connect to PostgreSQL: {e}")
        raise


def load_to_csv(df: pd.DataFrame, output_path: str = "data/processed/heart_clean.csv") -> None:
    """
    Saves the DataFrame as a CSV file (audit / fallback).

    Parameters
    ----------
    df : pd.DataFrame
        Transformed DataFrame.
    output_path : str
        Destination file path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"CSV saved to {output_path}")


def load(df: pd.DataFrame) -> None:
    """
    Runs both load targets: PostgreSQL + CSV.
    CSV load always runs; Postgres load is skipped if DB_PASSWORD is not set,
    which makes the pipeline usable without Docker for quick local testing.
    """
    load_to_csv(df)

    if os.getenv("DB_PASSWORD"):
        load_to_postgres(df)
    else:
        logger.warning(
            "DB_PASSWORD not set — skipping PostgreSQL load. "
            "Set it in .env or docker-compose.yml to enable."
        )
