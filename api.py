"""
FastAPI application entry point for Vercel deployment
This file imports and exposes the FastAPI app from server.py
"""

import sys
import os

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the FastAPI app from server.py
from server import app

# Vercel requires the app to be exported as 'app'
__all__ = ["app"]
