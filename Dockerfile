# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for database drivers
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    postgresql-client \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for SQLite database
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONPATH=/app
ENV CONTACT_MANAGER_DISABLE_UI=0

# Expose port (optional, for future web interface)
EXPOSE 8000

# Default command
CMD ["python", "main.py"]
