# Base image
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all code, including bootstrap_admin.py
COPY . /app

# Create uploads folder
RUN mkdir -p /app/static/uploads

EXPOSE 5001

ENV FLASK_ENV=production

# Default command is Flask app
CMD ["python", "run.py"]
