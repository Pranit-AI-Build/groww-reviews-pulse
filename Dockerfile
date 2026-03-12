# Dockerfile for Groww Reviews Weekly Pulse
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install schedule

# Copy all project files
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port for web dashboard
EXPOSE 8000

# Create startup script
RUN echo '#!/bin/bash\npython -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &\npython scheduler.py\n' > /app/start.sh && chmod +x /app/start.sh

# Command to run both web server and scheduler
CMD ["/app/start.sh"]
