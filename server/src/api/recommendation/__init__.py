from fastapi import APIRouter

from src.api.recommendation.drug import router as drug_router

# Создаем роутер для рекомендаций
router = APIRouter(
    prefix="/recommendation",
)

# Подключаем роутеры
router.include_router(drug_router)


__all__ = ["router"] 