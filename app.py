import os
from fastapi import FastAPI, Request, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pathlib import Path
import logging
from typing import Any, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Doctor API",
    description="AI-powered disease prediction and health information system",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Get the root directory
BASE_DIR = Path(__file__).parent

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Mount static files
static_dir = BASE_DIR / "static"
if not static_dir.exists():
    static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Setup templates
template_dir = BASE_DIR / "templates"
if not template_dir.exists():
    template_dir.mkdir(parents=True, exist_ok=True)
templates = Jinja2Templates(directory=str(template_dir))

# Include API routers
from backend.app.routers import health, predict

# API v1 routes
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(predict.router, prefix="/predict", tags=["predict"])
app.include_router(api_router)

# Root endpoint
@app.get("/", include_in_schema=False)
async def root() -> Dict[str, str]:
    """Root endpoint that provides API information"""
    return {
        "message": "Welcome to AI Doctor API",
        "docs": "/api/docs",
        "version": "1.0.0"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for uncaught exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
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
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {path}")
    
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
        port=int(os.getenv("PORT", 8000)),
        reload=True,
        log_level="info",
        workers=int(os.getenv("WEB_CONCURRENCY", 1)),
    )