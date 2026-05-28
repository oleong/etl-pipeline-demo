"""
test_transform.py
==================
Unit tests for the transformation stage.

Run with:
    pytest tests/

Author  : Oscar León
"""

import pandas as pd
import pytest
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from transform import (
    rename_columns,
    handle_missing,
    cast_types,
    derive_target,
    normalise_features,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def raw_df():
    """Minimal synthetic DataFrame that mimics the UCI CSV."""
    return pd.DataFrame({
        "age": [52, 44, 61],
        "sex": [1, 0, 1],
        "cp": [0, 1, 3],
        "trestbps": [125, 130, 148],
        "chol": [212, 219, 203],
        "fbs": [0, 0, 0],
        "restecg": [1, 0, 1],
        "thalach": [168, 188, 161],
        "exang": [0, 0, 0],
        "oldpeak": [1.0, 0.0, 0.0],
        "slope": [2, 2, 2],
        "ca": [2, 0, 1],
        "thal": [3, 2, 3],
        "target": [0, 0, 2],
    })


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_rename_columns(raw_df):
    df = rename_columns(raw_df)
    assert "age" in df.columns
    assert "resting_bp" in df.columns
    assert "cholesterol" in df.columns
    assert "trestbps" not in df.columns, "Original column should be renamed"


def test_handle_missing_drops_question_marks():
    df = pd.DataFrame({"a": [1, "?", 3], "b": [4, 5, 6]})
    df_clean = handle_missing(df)
    assert len(df_clean) == 2


def test_derive_target_binary(raw_df):
    df = rename_columns(raw_df)
    df = derive_target(df)
    assert "heart_disease" in df.columns
    assert set(df["heart_disease"].unique()).issubset({0, 1})
    assert "target" not in df.columns


def test_normalise_features_range(raw_df):
    df = rename_columns(raw_df)
    df = cast_types(df)
    df = normalise_features(df)
    for col in ["age", "resting_bp", "cholesterol"]:
        assert df[col].between(0, 1).all(), f"{col} out of [0,1] range"


def test_full_transform_shape(raw_df):
    from transform import transform
    df = transform(raw_df)
    assert len(df) == len(raw_df)       # no rows lost on clean data
    assert "heart_disease" in df.columns
    assert "target" not in df.columns
