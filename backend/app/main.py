from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .routers import health, predict

app = FastAPI(
    title="AI Doctor API",
    description="API for AI Doctor application that provides disease prediction and health recommendations",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(predict.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to AI Doctor API"}
