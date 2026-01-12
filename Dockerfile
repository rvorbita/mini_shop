# Use Python 3.10 slim for smaller image size
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for building packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads folder (for static files)
RUN mkdir -p /app/static/uploads

# Expose Flask port
EXPOSE 5001

# Set environment variable for Flask
ENV FLASK_ENV=production

# Use Gunicorn for production server
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "run:app"]
