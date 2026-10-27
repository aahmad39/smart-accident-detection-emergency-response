# Production Dockerfile for Smart Accident Response System on Azure App Service
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr and writing bytecode
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    FLASK_ENV=production

# Install system dependencies & Microsoft ODBC Driver for Azure SQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Run as non-root user for DevSecOps security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Run with Gunicorn production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--timeout", "60", "run:app"]
