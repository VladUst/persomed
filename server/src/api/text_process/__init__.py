from fastapi import APIRouter

from src.api.text_process.text_process import router as extraction_router

# Create main router for text processing API
router = APIRouter(prefix="/text-process")

# Include sub-routers
router.include_router(extraction_router)

__all__ = ["router"] 