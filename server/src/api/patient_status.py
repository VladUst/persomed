from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_depends import get_async_db
from src.schemas.patient_status import PatientStatusResponse
from src.services.patient_status import get_patient_status

# Создаем роутер для статуса пациента
patient_status_router = APIRouter(
    prefix="/patient-status",
    tags=["Статус пациента"]
)


@patient_status_router.get(
    "/", 
    response_model=PatientStatusResponse, 
    status_code=status.HTTP_200_OK,
    summary="Получить полный статус пациента"
)
async def get_status(db: AsyncSession = Depends(get_async_db)):
    """
    Получение полного статуса пациента.
    
    Этот эндпоинт объединяет информацию из разных источников для формирования полного представления о текущем состоянии пациента:
    
    - **Симптомы**: Текущие и недавние симптомы, автоматически извлеченные из анамнезов
    - **Заболевания**: Текущие заболевания пациента (5 последних из истории болезней)
    - **Оценки рисков**: Уровни рисков по различным категориям заболеваний
    - **Подозрения**: Подозреваемые заболевания, требующие дополнительной диагностики
    - **Факторы риска**: Факторы риска, полученные из сервиса анализа рисков
    - **Препараты**: Текущие назначенные препараты с дозировками
    - **Рекомендации**: Общие рекомендации по образу жизни и лечению
    
    Returns:
      Полный набор данных о состоянии пациента в структурированном виде
    """
    status_data = await get_patient_status(db)
    return {"status": status_data} 