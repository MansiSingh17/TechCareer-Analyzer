from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
import os

from backend.api import career, salary, trends, skills
from backend.utils.logger import setup_logger
from ml.inference.model_manager import ModelManager

load_dotenv()
logger = setup_logger(__name__)

# Initialize model manager globally
model_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load ML models
    global model_manager
    logger.info("Loading ML models...")
    model_manager = ModelManager()
    try:
        await model_manager.load_models()
        logger.info("Models loaded successfully")
    except Exception as e:
        logger.warning(f"Some models failed to load: {e}")
    
    yield
    
    # Shutdown: Clean up resources
    logger.info("Shutting down...")

app = FastAPI(
    title="TechCareer Analyzer API",
    description="ML-powered career path prediction and analysis",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(career.router, prefix="/api/career", tags=["career"])
app.include_router(salary.router, prefix="/api/salary", tags=["salary"])
app.include_router(trends.router, prefix="/api/trends", tags=["trends"])
app.include_router(skills.router, prefix="/api/skills", tags=["skills"])

@app.get("/")
async def root():
    return {
        "message": "TechCareer Analyzer API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "http://127.0.0.1:8000/docs",
            "health": "http://127.0.0.1:8000/health",
            "career": "/api/career",
            "salary": "/api/salary",
            "trends": "/api/trends",
            "skills": "/api/skills"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": model_manager is not None and model_manager.models_ready()
    }

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("DEBUG_MODE", "True").lower() == "true"
    )
