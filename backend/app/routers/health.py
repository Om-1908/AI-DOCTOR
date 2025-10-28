from fastapi import APIRouter, status, HTTPException
from typing import Dict, Any
import sys
from pathlib import Path

router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

@router.get("", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, Any]:
    """
    Comprehensive health check endpoint
    
    Returns:
        Dict with status and system information
    """
    try:
        # Basic system information
        system_info = {
            "status": "healthy",
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
            "api_version": "1.0.0"
        }
        
        # Check critical paths
        paths_to_check = [
            Path("Models/svc.pkl"),
            Path("Data.csv/symptoms_df.csv"),
            Path("Data.csv/Precautions_df.csv"),
            Path("Data.csv/Description.csv")
        ]
        
        missing_files = [str(path) for path in paths_to_check if not path.exists()]
        
        if missing_files:
            system_info["status"] = "degraded"
            system_info["missing_files"] = missing_files
        
        return system_info
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Health check failed: {str(e)}"
        )

@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check() -> Dict[str, str]:
    """
    Readiness check for Kubernetes/load balancers
    
    Returns:
        Dict with readiness status
    """
    try:
        # Add any readiness checks here (e.g., database connection)
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service not ready: {str(e)}"
        )

@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check for Kubernetes/load balancers
    
    Returns:
        Dict with liveness status
    """
    return {"status": "alive"}
