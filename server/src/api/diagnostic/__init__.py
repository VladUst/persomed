from fastapi import APIRouter

from src.api.diagnostic.prediction import router as prediction_router

# Создаем роутер для диагностики
router = APIRouter(
    prefix="/diagnostic",
)

# Подключаем роутеры
router.include_router(prediction_router)


__all__ = ["router"] 