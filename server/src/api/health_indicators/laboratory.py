from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_depends import get_async_db
from src.schemas.health_indicators import DetailedInfo, DetailedInfoCreate
from src.repositories.health_indicators import LaboratoryInfoRepository


laboratory_router = APIRouter(
    prefix="/laboratory",
    tags=["Лабораторные измерения"]
)


@laboratory_router.get("/", response_model=List[DetailedInfo], summary="Получить все лабораторные измерения")
async def get_all_laboratory_info(db: AsyncSession = Depends(get_async_db),):
    """
    Получение всех записей лабораторных измерений.
    
    Возвращает список всех записей лабораторных измерений.
    """
    repository = LaboratoryInfoRepository(db)
    return await repository.get_all()


@laboratory_router.get("/{id}", response_model=DetailedInfo, summary="Получить лабораторное измерение по ID")
async def get_laboratory_info(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Получение конкретной записи лабораторного измерения по её ID.
    
    - **id**: Уникальный идентификатор лабораторного измерения
    
    Возвращает запись лабораторного измерения, если оно найдено, иначе выдает ошибку 404.
    """
    repository = LaboratoryInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Лабораторное измерение с ID {id} не найдено"
        )
    return item


@laboratory_router.post("/", response_model=DetailedInfo, status_code=status.HTTP_201_CREATED, summary="Создать лабораторное измерение")
async def create_laboratory_info(
    data: DetailedInfoCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Создание нового лабораторного измерения.
    
    - **name**: Название показателя (обязательно)
    - **value**: Значение показателя (обязательно)
    - **canonical_name**: Каноническое название показателя (опционально)
    - **unit**: Единица измерения (опционально)
    - **date**: Дата измерения (опционально)
    - **target_level_min**: Минимальное допустимое значение (опционально)
    - **target_level_max**: Максимальное допустимое значение (опционально)
    
    Возвращает созданное лабораторное измерение с присвоенным ID.
    """
    repository = LaboratoryInfoRepository(db)
    return await repository.create(data.model_dump())


@laboratory_router.put("/{id}", response_model=DetailedInfo, summary="Обновить лабораторное измерение")
async def update_laboratory_info(id: int, data: DetailedInfoCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Обновление существующей записи лабораторного измерения.
    
    - **id**: Уникальный идентификатор записи для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленную запись лабораторного измерения, если она найдена, иначе выдает ошибку 404.
    """
    repository = LaboratoryInfoRepository(db)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Лабораторное измерение с ID {id} не найдено"
        )
    return await repository.update(id, data.model_dump())


@laboratory_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить лабораторное измерение")
async def delete_laboratory_info(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Удаление записи лабораторного измерения.
    
    - **id**: Уникальный идентификатор записи для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = LaboratoryInfoRepository(db)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Лабораторное измерение с ID {id} не найдено"
        ) 