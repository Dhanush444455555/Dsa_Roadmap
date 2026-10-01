FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run data seeding and start server
EXPOSE 8000

CMD ["sh", "-c", "python -m app.seed && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
