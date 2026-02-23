from fastapi import APIRouter

from src.api.text_processing.text_processing import text_processing_router

router = APIRouter(prefix="/text-processing")

router.include_router(text_processing_router)

__all__ = ["router"] 