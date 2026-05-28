"""
pipeline.py — Orchestrator
===========================
Runs the three ETL stages in sequence and logs timing info.

Usage:
    python src/pipeline.py
    python src/pipeline.py --input data/raw/heart.csv

Author  : Oscar León
"""

import argparse
import logging
import time

from extract import load_csv
from transform import transform
from load import load

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def run_pipeline(input_path: str) -> None:
    logger.info("=" * 50)
    logger.info("ETL PIPELINE STARTED")
    logger.info("=" * 50)

    # ── Stage 1: Extract ──────────────────────────────
    t0 = time.time()
    logger.info("[1/3] EXTRACT — reading source data")
    df_raw = load_csv(input_path)
    logger.info(f"      Done in {time.time() - t0:.2f}s")

    # ── Stage 2: Transform ────────────────────────────
    t1 = time.time()
    logger.info("[2/3] TRANSFORM — cleaning and enriching")
    df_clean = transform(df_raw)
    logger.info(f"      Done in {time.time() - t1:.2f}s")

    # ── Stage 3: Load ─────────────────────────────────
    t2 = time.time()
    logger.info("[3/3] LOAD — writing to destinations")
    load(df_clean)
    logger.info(f"      Done in {time.time() - t2:.2f}s")

    total = time.time() - t0
    logger.info("=" * 50)
    logger.info(f"PIPELINE COMPLETE — total time: {total:.2f}s")
    logger.info("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the ETL pipeline.")
    parser.add_argument(
        "--input",
        default="data/raw/heart.csv",
        help="Path to the raw CSV file (default: data/raw/heart.csv)",
    )
    args = parser.parse_args()
    run_pipeline(args.input)
