FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Create uploads folder and run bootstrap admin
RUN mkdir -p static/uploads && \
    python bootstrap_admin.py

# Expose port
EXPOSE 5001

# Environment variable
ENV FLASK_ENV=production

# Production-ready entrypoint
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "run:app"]
