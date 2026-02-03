# ================================
# Base image (small & stable)
# ================================
FROM python:3.11-slim

# ================================
# Environment settings
# ================================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ================================
# System dependencies
# ffmpeg is REQUIRED for audio
# ================================
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ================================
# Set working directory
# ================================
WORKDIR /app

# ================================
# Install Python dependencies
# ================================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ================================
# Copy application code
# ================================
COPY . .

# ================================
# Cloud Run port
# ================================
EXPOSE 8080

# ================================
# Start FastAPI (Cloud Run compatible)
# ================================
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
