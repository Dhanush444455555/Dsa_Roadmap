"""
Vercel serverless entry point for DSA Roadmap AI FastAPI backend.
Vercel uses ASGI serverless — no uvicorn process, just the app object.
SQLite is stored in /tmp (Vercel's writable temp dir).
"""
import sys
import os

# Make sure our backend app is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

# Point SQLite to /tmp so Vercel's read-only filesystem doesn't block writes
os.environ.setdefault("DATABASE_URL", "sqlite:////tmp/dsa_pathfinder.db")

from backend.app.main import app  # noqa: E402 — import after path setup
