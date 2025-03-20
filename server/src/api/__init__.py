from fastapi import APIRouter
from src.api.tasks import router as tasks_router

main_router = APIRouter()

main_router.include_router(tasks_router)
