# ETL Pipeline Demo — Heart Disease Dataset

A step-by-step demo of a production-style ETL pipeline built with Python, PostgreSQL and Docker.
Designed as a teaching resource for distributed data systems courses.

---

## What this project covers

| Stage | What you learn |
|-------|----------------|
| **Extract** | Reading CSV files with pandas, basic I/O patterns |
| **Transform** | Data cleaning, type casting, feature engineering, normalisation |
| **Load** | Writing to a relational database with SQLAlchemy |
| **Orchestration** | Connecting stages into a single runnable script |
| **Containerisation** | Docker + Docker Compose for reproducible environments |
| **Testing** | Unit tests for transformation logic with pytest |

---

## Dataset

[UCI Heart Disease Dataset (Cleveland, 1988)](https://archive.ics.uci.edu/dataset/45/heart+disease)

303 patient records, 13 clinical features, 1 binary target.
Widely used in data science education. No registration required to download.

```
data/
└── raw/
    └── heart.csv          ← place the downloaded file here
```

---

## Tech stack

- Python 3.11
- pandas 2.2, scikit-learn 1.4
- PostgreSQL 15 (via Docker)
- SQLAlchemy 2.0 + psycopg2
- Docker & Docker Compose
- pytest

---

## Project structure

```
etl-pipeline-demo/
├── src/
│   ├── extract.py          # Stage 1 — load raw CSV
│   ├── transform.py        # Stage 2 — clean & enrich
│   ├── load.py             # Stage 3 — write to Postgres + CSV
│   └── pipeline.py         # Orchestrator — runs all 3 stages
├── tests/
│   └── test_transform.py   # Unit tests for transform stage
├── data/
│   ├── raw/                # Place source CSV here (git-ignored)
│   └── processed/          # Output CSV written here
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## Quick start

### Option A — Docker (recommended)

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/etl-pipeline-demo.git
cd etl-pipeline-demo

# 2. Download the dataset and place it at data/raw/heart.csv
#    https://archive.ics.uci.edu/dataset/45/heart+disease

# 3. Copy the env file
cp .env.example .env

# 4. Build and run
docker compose up --build
```

You should see output similar to:

```
etl_pipeline  | 10:22:01 | INFO     | ETL PIPELINE STARTED
etl_pipeline  | 10:22:01 | INFO     | [1/3] EXTRACT — reading source data
etl_pipeline  | 10:22:01 | INFO     | Loaded 303 rows and 14 columns from data/raw/heart.csv
etl_pipeline  | 10:22:01 | INFO     | [2/3] TRANSFORM — cleaning and enriching
etl_pipeline  | 10:22:01 | INFO     | Transformation complete. Final shape: (303, 13)
etl_pipeline  | 10:22:01 | INFO     | [3/3] LOAD — writing to destinations
etl_pipeline  | 10:22:01 | INFO     | CSV saved to data/processed/heart_clean.csv
etl_pipeline  | 10:22:01 | INFO     | Loaded 303 rows into table 'heart_disease'.
etl_pipeline  | 10:22:01 | INFO     | PIPELINE COMPLETE — total time: 0.84s
```

After it finishes, `data/processed/heart_clean.csv` will be on your host machine.

To inspect the database:

```bash
docker exec -it etl_postgres psql -U etl_user -d etl_demo -c "SELECT * FROM heart_disease LIMIT 5;"
```

---

### Option B — Local Python (no Docker)

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place the dataset at data/raw/heart.csv

# 4. Run the pipeline
#    Without DB_PASSWORD set, the Postgres step is skipped automatically.
#    A clean CSV will still be written to data/processed/
python src/pipeline.py
```

---

## Running the tests

```bash
pytest tests/ -v
```

Expected output:

```
tests/test_transform.py::test_rename_columns PASSED
tests/test_transform.py::test_handle_missing_drops_question_marks PASSED
tests/test_transform.py::test_derive_target_binary PASSED
tests/test_transform.py::test_normalise_features_range PASSED
tests/test_transform.py::test_full_transform_shape PASSED

5 passed in 0.41s
```

---

## Understanding the transformation

The transform stage applies five steps in order:

```
raw DataFrame
    │
    ├─ 1. rename_columns()       cp → chest_pain_type, trestbps → resting_bp ...
    ├─ 2. handle_missing()       replace '?' → NaN, drop incomplete rows
    ├─ 3. cast_types()           ensure numeric dtypes after cleaning
    ├─ 4. derive_target()        target (0–4) → heart_disease (0 or 1)
    └─ 5. normalise_features()   MinMaxScaler on age, bp, cholesterol, hr, st_depression
```

Each step is an isolated function — easy to test, swap, or extend independently.

---

## Extending this project

Some ideas if you want to go further:

- **Add a Jupyter notebook** with exploratory analysis of the cleaned data
- **Replace the CSV source** with an API call (Open-Meteo, CoinGecko, etc.)
- **Add a second load target** — MongoDB, BigQuery, or a REST endpoint
- **Schedule the pipeline** with Apache Airflow or a simple cron job
- **Add data validation** with Great Expectations or Pydantic models
- **Build a dashboard** on top of the PostgreSQL table with Streamlit

---

## References

- Detrano, R. et al. (1989). *International application of a new probability algorithm for the diagnosis of coronary artery disease*. American Journal of Cardiology, 64(5), 304–310.
- UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/45/heart+disease

---

## License

MIT — free to use for teaching and personal projects.
