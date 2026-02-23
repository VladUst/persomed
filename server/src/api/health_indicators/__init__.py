from fastapi import APIRouter

from src.api.health_indicators.general import general_router
from src.api.health_indicators.laboratory import laboratory_router
from src.api.health_indicators.vaccinations import vaccinations_router
from src.api.health_indicators.allergies import allergies_router
from src.api.health_indicators.family_history import family_history_router
from src.api.health_indicators.lifestyle import lifestyle_router

router = APIRouter(
    prefix="/health-indicators",
)

router.include_router(general_router)
router.include_router(laboratory_router)
router.include_router(vaccinations_router)
router.include_router(allergies_router)
router.include_router(family_history_router)
router.include_router(lifestyle_router)


__all__ = ["router"] 