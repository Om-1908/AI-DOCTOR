import os
from fastapi import FastAPI, Request, status, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import logging
import sys
from typing import Any, Dict
import os

# Determine base directory
BASE_DIR = Path(__file__).parent

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent / "backend"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Doctor API",
    description="API for AI Doctor application",
    version="1.0.0",
    docs_url="/",  # Serve docs at root
    redoc_url=None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up static files
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True, parents=True)
app.mount("/static", StaticFiles(directory=str(static_dir), html=True), name="static")

# Set up templates
template_dir = Path(__file__).parent / "templates"
template_dir.mkdir(exist_ok=True, parents=True)
templates = Jinja2Templates(directory=str(template_dir))

# Include API routers
from backend.app.routers import health, predict

# API v1 routes
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(predict.router, prefix="/predict", tags=["predict"])
app.include_router(api_router)

# Root endpoint - Now serves the Swagger UI directly
@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint - Serves the API documentation"""
    return {
        "message": "AI Doctor API is running. Use the interactive documentation below.",
        "api_docs": "/"
    }

# Global exception handler
from fastapi.responses import JSONResponse
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for uncaught exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": f"Internal server error: {str(exc)}"},
    )

# Health check endpoint for load balancers
@app.get("/health", include_in_schema=False)
async def health_check() -> Dict[str, str]:
    """Health check endpoint for load balancers"""
    return {"status": "ok"}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run startup tasks"""
    logger.info("Starting AI Doctor API...")
    
    # Create necessary directories if they don't exist
    for directory in ["Models", "Data.csv", "static", "templates"]:
        path = BASE_DIR / directory
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory ready: {path}")
    
    # Verify important files exist
    required_files = [
        BASE_DIR / "Models" / "svc.pkl",
        BASE_DIR / "Data.csv" / "symptoms_df.csv",
        BASE_DIR / "Data.csv" / "training.csv"
    ]
    
    for file_path in required_files:
        if not file_path.exists():
            logger.warning(f"Required file not found: {file_path}")
    
    logger.info("AI Doctor API started successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run shutdown tasks"""
    logger.info("Shutting down AI Doctor API...")

if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "app:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 7860)),  # Default port for Hugging Face Spaces
        reload=True,
        log_level="info",
        workers=int(os.getenv("WEB_CONCURRENCY", 1)),
    )