"""
transform.py — Stage 2: Data Transformation
=============================================
Cleans and prepares the raw DataFrame for loading.

Transformation steps applied:
  1. Rename columns to human-readable names
  2. Replace coded missing values (e.g. "?") with NaN
  3. Drop rows with missing values
  4. Cast columns to correct dtypes
  5. Derive a binary target column (heart_disease: 0 / 1)
  6. Normalise continuous features to [0, 1]

Author  : Oscar León
"""

import logging
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

logger = logging.getLogger(__name__)

# Mapping from original UCI column names to readable names
COLUMN_NAMES = {
    "age": "age",
    "sex": "sex",
    "cp": "chest_pain_type",
    "trestbps": "resting_bp",
    "chol": "cholesterol",
    "fbs": "fasting_blood_sugar",
    "restecg": "resting_ecg",
    "thalach": "max_heart_rate",
    "exang": "exercise_angina",
    "oldpeak": "st_depression",
    "slope": "st_slope",
    "ca": "num_vessels",
    "thal": "thalassemia",
    "target": "target",
}

CONTINUOUS_FEATURES = [
    "age",
    "resting_bp",
    "cholesterol",
    "max_heart_rate",
    "st_depression",
]


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to human-readable names where applicable."""
    df = df.rename(columns={k: v for k, v in COLUMN_NAMES.items() if k in df.columns})
    logger.info("Columns renamed.")
    return df


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Replace '?' placeholders and drop rows with any NaN."""
    initial_rows = len(df)
    df = df.replace("?", pd.NA)
    df = df.dropna()
    dropped = initial_rows - len(df)
    if dropped > 0:
        logger.warning(f"Dropped {dropped} rows with missing values.")
    else:
        logger.info("No missing values found.")
    return df


def cast_types(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure numeric columns have the right dtype after cleaning."""
    numeric_cols = [
        "age", "resting_bp", "cholesterol", "max_heart_rate",
        "st_depression", "num_vessels",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna()  # drop any rows that became NaN after casting
    logger.info("Column types validated.")
    return df


def derive_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    The UCI target column contains values 0-4.
    We convert this to a binary label:
      0  → no disease
      1+ → disease present
    """
    if "target" in df.columns:
        df["heart_disease"] = (df["target"] > 0).astype(int)
        df = df.drop(columns=["target"])
        logger.info("Binary target column 'heart_disease' derived.")
    return df


def normalise_features(df: pd.DataFrame) -> pd.DataFrame:
    """Scale continuous features to the [0, 1] range using MinMaxScaler."""
    cols_to_scale = [c for c in CONTINUOUS_FEATURES if c in df.columns]
    scaler = MinMaxScaler()
    df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])
    logger.info(f"Normalised columns: {cols_to_scale}")
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full transformation pipeline. Applies all steps in order.

    Parameters
    ----------
    df : pd.DataFrame
        Raw DataFrame as returned by extract.load_csv().

    Returns
    -------
    pd.DataFrame
        Clean, transformed DataFrame ready for loading.
    """
    df = rename_columns(df)
    df = handle_missing(df)
    df = cast_types(df)
    df = derive_target(df)
    df = normalise_features(df)
    logger.info(f"Transformation complete. Final shape: {df.shape}")
    return df
