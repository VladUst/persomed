from fastapi import APIRouter

from src.api.medical_documents.analyzes import analyzes_router
from src.api.medical_documents.other import other_router
from src.api.medical_documents.diseases_history import diseases_history_router
from src.api.medical_documents.recommendations import recommendations_router

router = APIRouter(
    prefix="/medical-documents",
)

router.include_router(analyzes_router)
router.include_router(other_router)
router.include_router(diseases_history_router)
router.include_router(recommendations_router)


__all__ = ["router"] 