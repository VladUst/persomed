from fastapi import APIRouter

from src.api.health_indicators import router as health_indicators_router
from src.api.medical_documents import router as medical_documents_router
from src.api.tasks import router as tasks_router
from src.api.diagnostic import router as diagnostic_router

# Создаем основной роутер API
router = APIRouter(
    prefix="/api"
)

# Подключаем роутеры
router.include_router(health_indicators_router)
router.include_router(medical_documents_router)
router.include_router(tasks_router)
router.include_router(diagnostic_router)

__all__ = ["router"]
