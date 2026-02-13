
from fastapi import APIRouter
from app.schemas.common import HealthCheck

router = APIRouter()

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """
    Check if the API is running and healthy.
    """
    return {
        "status": "ok",
        "version": "0.1.0"
    }
