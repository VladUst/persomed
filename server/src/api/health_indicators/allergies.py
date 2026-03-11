from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_depends import get_async_db
from src.schemas.health_indicators import AllergyInfo, AllergyInfoCreate
from src.repositories.health_indicators import AllergyInfoRepository

allergies_router = APIRouter(
    prefix="/allergies",
    tags=["Аллергии и непереносимости"]
)


@allergies_router.get("/", response_model=List[AllergyInfo], summary="Получить всю информацию об аллергиях")
async def get_all_allergies_info(patient_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Получение всех записей об аллергиях.
    
    Возвращает список всех записей об аллергиях.
    """
    repository = AllergyInfoRepository(db)
    return await repository.get_all_by_patient(patient_id)


@allergies_router.get("/{id}", response_model=AllergyInfo, summary="Получить информацию об аллергии по ID")
async def get_allergies_info(patient_id: int, id: int, db: AsyncSession = Depends(get_async_db)):
    repository = AllergyInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Запись об аллергии с ID {id} не найдена")
    return item


@allergies_router.post("/", response_model=AllergyInfo, status_code=status.HTTP_201_CREATED, summary="Создать информацию об аллергии")
async def create_allergies_info(
    patient_id: int,
    data: AllergyInfoCreate,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Создание новой записи об аллергии.
    
    - **name**: Название аллергии (обязательно)
    - **value**: Измерение (обязательно)
    - **canonical_name**: Каноническое название аллергии (опционально)
    - **unit**: Единица измерения (опционально)
    - **date**: Дата выявления (опционально)
    - **target_level_min**: Минимальное допустимое значение (опционально)
    - **target_level_max**: Максимальное допустимое значение (опционально)
    
    Возвращает созданную запись об аллергии с присвоенным ID.
    """
    repository = AllergyInfoRepository(db)
    return await repository.create({**data.model_dump(), "patient_id": patient_id})


@allergies_router.put("/{id}", response_model=AllergyInfo, summary="Обновить запись об аллергии")
async def update_allergies_info(patient_id: int, id: int, data: AllergyInfoCreate, db: AsyncSession = Depends(get_async_db)):
    repository = AllergyInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Запись об аллергии с ID {id} не найдена")
    return await repository.update(id, data.model_dump())


@allergies_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить запись об аллергии")
async def delete_allergies_info(patient_id: int, id: int, db: AsyncSession = Depends(get_async_db)):
    repository = AllergyInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Запись об аллергии с ID {id} не найдена")
    await repository.delete(id) 