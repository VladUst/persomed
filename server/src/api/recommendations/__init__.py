from fastapi import APIRouter

from src.api.recommendations.recommendations import recommendations_router

router = APIRouter(
    prefix="/recommendations",
)

router.include_router(recommendations_router)


__all__ = ["router"] 