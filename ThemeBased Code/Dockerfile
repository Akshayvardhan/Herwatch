# Use lightweight Python 3.10 image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=5001 \
    TORCH_HOME=/tmp/torch \
    YOLO_CONFIG_DIR=/tmp/Ultralytics

# Install system dependencies for OpenCV, MediaPipe, PyTorch
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for Docker cache optimization
COPY requirements.txt .

# Install Python packages (using CPU torch wheels to keep build fast and compact)
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Copy application source code
COPY . .

# Expose port
EXPOSE 5001

# Command to run application using Gunicorn with gevent worker for WebSocket support
CMD ["sh", "-c", "gunicorn -k gevent -w 1 -b 0.0.0.0:${PORT:-5001} --timeout 120 app:app"]
