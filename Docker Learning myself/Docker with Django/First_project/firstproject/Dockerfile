FROM python:3.9-slim

WORKDIR /app

# Install only the PostgreSQL client (needed for health check)
RUN apt-get update && apt-get install -y postgresql-client && apt-get clean

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .