
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Configure writable model cache locations
ENV HOME=/home/appuser
ENV HF_HOME=/home/appuser/.cache/huggingface
ENV SENTENCE_TRANSFORMERS_HOME=/home/appuser/.cache/torch/sentence_transformers
ENV TORCH_HOME=/home/appuser/.cache/torch

WORKDIR /app

# Install Linux runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user with a valid home directory
RUN groupadd --system appgroup && \
    useradd --system --create-home \
    --home-dir /home/appuser \
    --gid appgroup appuser

# Install Python dependencies
COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# Copy application files
COPY --chown=appuser:appgroup . .

# Create writable directories
RUN mkdir -p \
    /app/data \
    /app/vectorstore \
    /home/appuser/.cache/huggingface \
    /home/appuser/.cache/torch \
    && chown -R appuser:appgroup /app /home/appuser

# Run application as non-root user
USER appuser

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.headless=true"]
