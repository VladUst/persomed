from fastapi import APIRouter

from src.api.health_indicators import router as health_indicators_router
from src.api.medical_documents import router as medical_documents_router
from src.api.tasks import router as tasks_router
from src.api.diagnostic import router as diagnostic_router
from src.api.recommendation import router as recommendation_router
from src.api.risk_analysis import router as risk_analysis_router
from src.api.text_process import router as text_process_router
from src.api.patient_status import patient_status_router

# Создаем основной роутер API
router = APIRouter(
    prefix="/api"
)

# Подключаем роутеры
router.include_router(health_indicators_router)
router.include_router(medical_documents_router)
router.include_router(tasks_router)
router.include_router(diagnostic_router)
router.include_router(recommendation_router)
router.include_router(risk_analysis_router)
router.include_router(text_process_router)
router.include_router(patient_status_router)

__all__ = ["router"]
