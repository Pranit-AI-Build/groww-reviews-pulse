"""WSGI entry point for PythonAnywhere."""
import sys
import os

# Add the backend directory to the path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.insert(0, path)

# Change to backend directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Import the FastAPI app
from app.main import app

# For PythonAnywhere WSGI
application = app
