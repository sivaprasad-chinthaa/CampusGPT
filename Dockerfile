
# Python base image
FROM python:3.11-slim

# Python runtime configuration
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Application directory
WORKDIR /app

# Install required Linux runtime library
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root application user
RUN groupadd --system appgroup && \
    useradd --system --gid appgroup appuser

# Copy dependency file first
COPY requirements.txt .

# Install all Python dependencies
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# Copy project files
COPY --chown=appuser:appgroup . .

# Run as non-root user
USER appuser

# Streamlit port
EXPOSE 8501

# Start Streamlit
CMD ["python", "-m", "streamlit", "run", "app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.headless=true"]
