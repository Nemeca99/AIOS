# CARMA: Cached Aided Retrieval Mycelium Architecture
# Production-ready container for reproducible testing

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p AI/personality/embedder_cache \
    && mkdir -p AI/personality/learning_data \
    && mkdir -p AI/personality/master_test_results \
    && mkdir -p AI/personality/learning_results \
    && mkdir -p telemetry_data \
    && mkdir -p ablation_results \
    && mkdir -p human_eval \
    && mkdir -p seed_corpus \
    && mkdir -p carma_data

# Set environment variables
ENV PYTHONPATH=/app
ENV CARMA_BASE_DIR=/app/carma_data
ENV LM_STUDIO_URL=http://host.docker.internal:1234/v1

# Expose port for Streamlit (if used)
EXPOSE 8501

# Create a non-root user
RUN useradd -m -u 1000 carma && chown -R carma:carma /app
USER carma

# Default command - run human evaluation prep
CMD ["python", "human_eval/human_eval_prep.py", "--sample", "--questions", "20"]
