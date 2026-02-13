
from fastapi import APIRouter
from app.api.endpoints import health, upload

api_router = APIRouter()

api_router.include_router(health.router, tags=["system"])
api_router.include_router(upload.router, prefix="/data", tags=["data"])
