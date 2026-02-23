from fastapi import APIRouter

from src.api.health_indicators import router as health_indicators_router
from src.api.medical_documents import router as medical_documents_router
from src.api.diagnostic import router as diagnostic_router
from src.api.recommendations import router as recommendations_router
from src.api.risk_analysis import router as risk_analysis_router
from src.api.text_processing import router as text_processing_router
from src.api.patient_status import router as patient_status_router

router = APIRouter(
    prefix="/api"
)

router.include_router(health_indicators_router)
router.include_router(medical_documents_router)
router.include_router(diagnostic_router)
router.include_router(recommendations_router)
router.include_router(risk_analysis_router)
router.include_router(text_processing_router)
router.include_router(patient_status_router)

__all__ = ["router"]
