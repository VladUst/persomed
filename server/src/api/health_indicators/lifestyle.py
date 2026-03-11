from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_depends import get_async_db
from src.schemas.health_indicators import LifestyleInfo, LifestyleInfoCreate
from src.repositories.health_indicators import LifestyleInfoRepository


# Создаем роутер для образа жизни
lifestyle_router = APIRouter(
    prefix="/lifestyle",
    tags=["Образ жизни"]
)


@lifestyle_router.get("/", response_model=List[LifestyleInfo], summary="Получить всю информацию об образе жизни")
async def get_all_lifestyle_info(patient_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Получение всех записей об образе жизни.
    
    Возвращает список всех записей об образе жизни.
    """
    repository = LifestyleInfoRepository(db)
    return await repository.get_all_by_patient(patient_id)


@lifestyle_router.get("/{id}", response_model=LifestyleInfo, summary="Получить информацию об образе жизни по ID")
async def get_lifestyle_info(patient_id: int, id: int, db: AsyncSession = Depends(get_async_db)):
    repository = LifestyleInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Запись об образе жизни с ID {id} не найдена")
    return item


@lifestyle_router.post("/", response_model=LifestyleInfo, status_code=status.HTTP_201_CREATED, summary="Создать информацию об образе жизни")
async def create_lifestyle_info(
    patient_id: int,
    data: LifestyleInfoCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Создание новой записи об образе жизни.
    
    - **name**: Название показателя (обязательно)
    - **value**: Измерение (обязательно)
    - **canonical_name**: Каноническое название показателя (опционально)
    - **unit**: Единица измерения (опционально)
    - **date**: Дата добавления информации (опционально)
    - **target_level_min**: Минимальное допустимое значение (опционально)
    - **target_level_max**: Максимальное допустимое значение (опционально)
    
    Возвращает созданную запись об образе жизни с присвоенным ID.
    """
    repository = LifestyleInfoRepository(db)
    return await repository.create({**data.model_dump(), "patient_id": patient_id})


@lifestyle_router.put("/{id}", response_model=LifestyleInfo, summary="Обновить запись об образе жизни")
async def update_lifestyle_info(patient_id: int, id: int, data: LifestyleInfoCreate, db: AsyncSession = Depends(get_async_db)):
    repository = LifestyleInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Запись об образе жизни с ID {id} не найдена")
    return await repository.update(id, data.model_dump())


@lifestyle_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить запись об образе жизни")
async def delete_lifestyle_info(patient_id: int, id: int, db: AsyncSession = Depends(get_async_db)):
    repository = LifestyleInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Запись об образе жизни с ID {id} не найдена")
    await repository.delete(id) 