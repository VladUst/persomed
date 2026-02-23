from fastapi import APIRouter

from src.api.risk_analysis.risk_analysis import risk_analysis_router

router = APIRouter(
    prefix="/risk-analysis",
)

router.include_router(risk_analysis_router)

__all__ = ["router"] 