from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_depends import get_async_db
from src.schemas.health_indicators import VaccinationInfo, VaccinationInfoCreate
from src.repositories.health_indicators import VaccinationInfoRepository


vaccinations_router = APIRouter(
    prefix="/vaccinations",
    tags=["Вакцинации и профилактические мероприятия"]
)


@vaccinations_router.get("/", response_model=List[VaccinationInfo], summary="Получить всю информацию о прививках")
async def get_all_vaccinations_info(patient_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Получение всех записей о прививках и профилактических мероприятиях.
    
    Возвращает список всех записей о прививках и профилактических мероприятиях.
    """
    repository = VaccinationInfoRepository(db)
    return await repository.get_all_by_patient(patient_id)


@vaccinations_router.get("/{id}", response_model=VaccinationInfo, summary="Получить информацию о прививке по ID")
async def get_vaccinations_info(patient_id: int, id: int, db: AsyncSession = Depends(get_async_db)):
    repository = VaccinationInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Запись о прививке с ID {id} не найдена")
    return item


@vaccinations_router.post("/", response_model=VaccinationInfo, status_code=status.HTTP_201_CREATED, summary="Создать информацию о прививке")
async def create_vaccinations_info(
    patient_id: int,
    data: VaccinationInfoCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Создание нового профилактического показателя.
    
    - **name**: Название показателя (обязательно)
    - **value**: Измерение (обязательно)
    - **canonical_name**: Каноническое название показателя (опционально)
    - **unit**: Единица измерения (опционально)
    - **date**: Дата измерения (опционально)
    - **target_level_min**: Минимальное допустимое значение (опционально)
    - **target_level_max**: Максимальное допустимое значение (опционально)
    
    Возвращает созданный профилактический показатель с присвоенным ID.
    """
    repository = VaccinationInfoRepository(db)
    return await repository.create({**data.model_dump(), "patient_id": patient_id})


@vaccinations_router.put("/{id}", response_model=VaccinationInfo, summary="Обновить информацию о прививке")
async def update_vaccinations_info(patient_id: int, id: int, data: VaccinationInfoCreate, db: AsyncSession = Depends(get_async_db)):
    repository = VaccinationInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Запись о прививке с ID {id} не найдена")
    return await repository.update(id, data.model_dump())


@vaccinations_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить информацию о прививке")
async def delete_vaccinations_info(patient_id: int, id: int, db: AsyncSession = Depends(get_async_db)):
    repository = VaccinationInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Запись о прививке с ID {id} не найдена")
    await repository.delete(id)