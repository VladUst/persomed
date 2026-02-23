from fastapi import APIRouter

from src.api.patient_status.patient_status import patient_status_router

router = APIRouter(prefix="/patient-status")

router.include_router(patient_status_router)

__all__ = ["router"] 