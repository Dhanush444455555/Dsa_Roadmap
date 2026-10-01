import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

from .database.session import engine, Base
from .database.models import Base
from .api.routes import router as api_router
from .api.ai_chat import router as ai_chat_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DSA Roadmap AI API",
    description="Intelligent DSA Preparation Roadmap Generator with Spaced Repetition and Weak-Topic Detection",
    version="1.0.0"
)

# CORS: Allow Vercel frontend + localhost dev
# Set ALLOWED_ORIGINS env var on Railway to your Vercel URL (comma-separated)
_raw_origins = os.getenv("ALLOWED_ORIGINS", "")
if _raw_origins:
    allow_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]
else:
    # Default: allow all (safe for dev / Railway first deploy)
    allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(api_router)
app.include_router(ai_chat_router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}"}
    )

@app.get("/")
def root():
    return {
        "message": "Welcome to DSA Roadmap AI API",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
