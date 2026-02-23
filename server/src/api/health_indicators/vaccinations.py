from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_depends import get_async_db
from src.schemas.health_indicators import VaccinationsInfo, VaccinationsInfoCreate
from src.repositories.health_indicators import VaccinationsInfoRepository


vaccinations_router = APIRouter(
    prefix="/vaccinations",
    tags=["Вакцинации и профилактические мероприятия"]
)


@vaccinations_router.get("/", response_model=List[VaccinationsInfo], summary="Получить всю информацию о прививках")
async def get_all_vaccinations_info(db: AsyncSession = Depends(get_async_db)):
    """
    Получение всех записей о прививках и профилактических мероприятиях.
    
    Возвращает список всех записей о прививках и профилактических мероприятиях.
    """
    repository = VaccinationsInfoRepository(db)
    return await repository.get_all()


@vaccinations_router.get("/{id}", response_model=VaccinationsInfo, summary="Получить информацию о прививке по ID")
async def get_vaccinations_info(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Получение конкретной записи о прививке/профилактике по её ID.
    
    - **id**: Уникальный идентификатор записи о прививке
    
    Возвращает запись о прививке/профилактике, если она найдена, иначе выдает ошибку 404.
    """
    repository = VaccinationsInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись о прививке с ID {id} не найдена"
        )
    return item


@vaccinations_router.post("/", response_model=VaccinationsInfo, status_code=status.HTTP_201_CREATED, summary="Создать информацию о прививке")
async def create_vaccinations_info(
    data: VaccinationsInfoCreate,
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
    repository = VaccinationsInfoRepository(db)
    return await repository.create(data.model_dump())


@vaccinations_router.put("/{id}", response_model=VaccinationsInfo, summary="Обновить информацию о прививке")
async def update_vaccinations_info(id: int, data: VaccinationsInfoCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Обновление существующей записи о прививке/профилактике.
    
    - **id**: Уникальный идентификатор записи для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленную запись о прививке/профилактике, если она найдена, иначе выдает ошибку 404.
    """
    repository = VaccinationsInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись о прививке с ID {id} не найдена"
        )
    return await repository.update(id, data.model_dump())


@vaccinations_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить информацию о прививке")
async def delete_vaccinations_info(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Удаление записи о прививке/профилактике.
    
    - **id**: Уникальный идентификатор записи для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = VaccinationsInfoRepository(db)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись о прививке с ID {id} не найдена"
        )