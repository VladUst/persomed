from fastapi import APIRouter

from src.api.risk_analysis.risk_factors import router as risk_factors_router

# Create a router for risk analysis
router = APIRouter(
    prefix="/risk-analysis",
)

# Include sub-routers
router.include_router(risk_factors_router)

__all__ = ["router"] 