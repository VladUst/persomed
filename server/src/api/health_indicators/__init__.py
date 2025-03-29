from fastapi import APIRouter

from src.api.health_indicators.general import general_router
from src.api.health_indicators.detailed import detailed_router
from src.api.health_indicators.preventive import preventive_router
from src.api.health_indicators.allergies import allergies_router
from src.api.health_indicators.family_history import family_history_router
from src.api.health_indicators.lifestyle import lifestyle_router

# Объединяем все роутеры показателей здоровья
router = APIRouter(
    prefix="/health-indicators",
)

# Добавляем все подроутеры
router.include_router(general_router)
router.include_router(detailed_router)
router.include_router(preventive_router)
router.include_router(allergies_router)
router.include_router(family_history_router)
router.include_router(lifestyle_router)


__all__ = ["router"] 