from fastapi import APIRouter

from src.api.diagnostic.diagnostic import diagnostic_router

router = APIRouter(
    prefix="/diagnostic",
)

router.include_router(diagnostic_router)


__all__ = ["router"] 