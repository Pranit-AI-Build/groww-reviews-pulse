#!/bin/bash
# Startup script for Groww Reviews Weekly Pulse

cd /opt/render/project/src

# Start web server in background
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &

# Start scheduler in foreground
python scheduler.py
