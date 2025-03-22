from fastapi import APIRouter
from src.api.tasks import router as tasks_router
from src.api.health_indicators import router as health_indicators_router
from src.api.medical_documents import router as medical_documents_router

main_router = APIRouter()

main_router.include_router(tasks_router)
main_router.include_router(health_indicators_router)
main_router.include_router(medical_documents_router)
