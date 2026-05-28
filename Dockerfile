FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed by psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command — can be overridden in docker-compose.yml
CMD ["python", "src/pipeline.py"]
