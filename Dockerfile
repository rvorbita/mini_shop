# # Base image
# FROM python:3.10-slim

# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# # Copy requirements
# COPY requirements.txt .

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Copy all code, including bootstrap_admin.py
# COPY . /app

# # Create uploads folder
# RUN mkdir -p /app/static/uploads

# EXPOSE 5001

# ENV FLASK_ENV=production

# # Default command is Flask app
# CMD ["python", "run.py"]

# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for building packages)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Dockerfile snippet
COPY bootstrap_admin.py /app/

# Run bootstrap admin script during image build
RUN python /app/bootstrap_admin.py

# Create uploads folder (ensure it exists)
RUN mkdir -p /app/static/uploads

# Expose port
EXPOSE 5001

# Set environment variable
ENV FLASK_ENV=production

# Use gunicorn for production instead of "python run.py"
# This is more stable for CI/CD pipelines
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "run:app"]
