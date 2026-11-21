from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router

app = FastAPI(
    title="GlobeWise API",
    description="AI-powered personal global life assistant backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "app": "GlobeWise API",
        "status": "running",
        "message": "Welcome to GlobeWise backend",
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "globewise-backend",
    }

app.include_router(api_router, prefix="/api/v1")

from globewise_live import router as live_router

app.include_router(live_router, prefix="/api")
