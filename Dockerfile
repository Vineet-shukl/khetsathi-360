# Universal production container for KhetSathi 360
# Compatible with Render, Hugging Face Spaces, Koyeb, Railway, and Cloud Run
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENABLE_ML_RESIDUAL=true

# Minimal curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application logic, pre-trained model artifacts, and frontend
COPY app/ ./app/
COPY artifacts/ ./artifacts/
COPY frontend/ ./frontend/

# Expose ports (8000 for standard, 7860 for Hugging Face)
EXPOSE 8000 7860

# Universal health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/api/v1/health || exit 1

# Start uvicorn with dynamic port detection
CMD ["sh", "-c", "uvicorn app.api:app --host 0.0.0.0 --port ${PORT:-8000}"]
