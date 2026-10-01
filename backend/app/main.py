import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

from .database.session import engine, Base
from .database.models import Base
from .api.routes import router as api_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DSA Roadmap AI API",
    description="Intelligent DSA Preparation Roadmap Generator with Spaced Repetition and Weak-Topic Detection",
    version="1.0.0"
)

# Enable CORS for Frontend React/Vite development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Router
app.include_router(api_router)

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
