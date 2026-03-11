from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_depends import get_async_db
from src.schemas.health_indicators import GeneralInfo, GeneralInfoCreate
from src.repositories.health_indicators import GeneralInfoRepository


general_router = APIRouter(
    prefix="/general",
    tags=["Общая информация о здоровье"]
)


@general_router.get("/", response_model=List[GeneralInfo], summary="Получить всю базовую информацию о здоровье")
async def get_all_general_info(patient_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Получение всех записей базовой информации о здоровье.
    
    Возвращает список всех записей базовой информации о здоровье.
    """
    repository = GeneralInfoRepository(db)
    return await repository.get_all_by_patient(patient_id)


@general_router.get("/{id}", response_model=GeneralInfo, summary="Получить базовую информацию о здоровье по ID")
async def get_general_info(patient_id: int, id: int, db: AsyncSession = Depends(get_async_db)):
    repository = GeneralInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Базовая информация с ID {id} не найдена")
    return item


@general_router.post("/", response_model=GeneralInfo, status_code=status.HTTP_201_CREATED, summary="Создать общий показатель здоровья")
async def create_general_info(
    patient_id: int,
    data: GeneralInfoCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Создание нового общего показателя здоровья.
    
    - **name**: Название показателя (обязательно)
    - **value**: Значение показателя (обязательно)
    - **canonical_name**: Каноническое название показателя (опционально)
    - **unit**: Единица измерения (опционально)
    - **date**: Дата измерения (опционально)
    - **target_level_min**: Минимальное допустимое значение (опционально)
    - **target_level_max**: Максимальное допустимое значение (опционально)
    
    Возвращает созданный показатель здоровья с присвоенным ID.
    """
    repository = GeneralInfoRepository(db)
    return await repository.create({**data.model_dump(), "patient_id": patient_id})


@general_router.put("/{id}", response_model=GeneralInfo, summary="Обновить базовую информацию о здоровье")
async def update_general_info(patient_id: int, id: int, data: GeneralInfoCreate, db: AsyncSession = Depends(get_async_db)):
    repository = GeneralInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Базовая информация с ID {id} не найдена")
    return await repository.update(id, data.model_dump())


@general_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить базовую информацию о здоровье")
async def delete_general_info(patient_id: int, id: int, db: AsyncSession = Depends(get_async_db)):
    repository = GeneralInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Базовая информация с ID {id} не найдена")
    await repository.delete(id) 