# -------------------------
# Base image
# -------------------------
FROM python:3.13-slim

# -------------------------
# Environment optimizations
# -------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# -------------------------
# System dependencies
# (needed for psycopg, cryptography, etc.)
# -------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# App setup
# -------------------------
WORKDIR /app

# Install Python dependencies first (cache-friendly)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# -------------------------
# Additional system dependencies
# -------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# Security: non-root user
# -------------------------
RUN useradd -m appuser
USER appuser


# -------------------------
# Healthcheck
# -------------------------
HEALTHCHECK --interval=30s --timeout=5s --retries=5 \
  CMD curl -f http://localhost:8000/health || exit 1

# -------------------------
# Runtime
# -------------------------
EXPOSE 8000

CMD ["gunicorn", "main:app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--timeout", "60"]
