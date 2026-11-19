# Universal production container for KhetSathi 360
# 100% Compatible with Hugging Face Spaces (Port 7860, UID 1000), Render, Koyeb, and Cloud Run
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENABLE_ML_RESIDUAL=true \
    PORT=7860

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

# Create non-root user (UID 1000) required by Hugging Face Spaces
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose ports (7860 for Hugging Face Spaces, 8000 for standard)
EXPOSE 7860 8000

# Universal health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-7860}/api/v1/health || exit 1

# Start uvicorn with dynamic port detection (defaults to 7860 for Hugging Face)
CMD ["sh", "-c", "uvicorn app.api:app --host 0.0.0.0 --port ${PORT:-7860}"]
