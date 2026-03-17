"""
Vercel Python runtime entry point for FastAPI application
This file imports and exposes the FastAPI app from server.py
"""

from server import app

# Vercel requires the app to be exported as 'app'
__all__ = ["app"]
