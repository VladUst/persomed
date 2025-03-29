from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.health_indicators.session import get_session
from src.schemas.health_indicators import LifestyleInfo, LifestyleInfoCreate
from src.repositories.health_indicators import LifestyleInfoRepository


# Создаем роутер для образа жизни
lifestyle_router = APIRouter(
    prefix="/lifestyle",
    tags=["Образ жизни"]
)


@lifestyle_router.get("/", response_model=List[LifestyleInfo], summary="Получить всю информацию об образе жизни")
async def get_all_lifestyle_info(session: AsyncSession = Depends(get_session)):
    """
    Получение всех записей об образе жизни.
    
    Возвращает список всех записей об образе жизни.
    """
    repository = LifestyleInfoRepository(session)
    return await repository.get_all()


@lifestyle_router.get("/{id}", response_model=LifestyleInfo, summary="Получить информацию об образе жизни по ID")
async def get_lifestyle_info(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретной записи об образе жизни по её ID.
    
    - **id**: Уникальный идентификатор записи об образе жизни
    
    Возвращает запись об образе жизни, если она найдена, иначе выдает ошибку 404.
    """
    repository = LifestyleInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись об образе жизни с ID {id} не найдена"
        )
    return item


@lifestyle_router.post("/", response_model=LifestyleInfo, status_code=status.HTTP_201_CREATED, summary="Создать информацию об образе жизни")
async def create_lifestyle_info(
    data: LifestyleInfoCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание новой записи об образе жизни.
    
    - **name**: Название показателя (обязательно)
    - **value**: Значение показателя (обязательно)
    - **canonical_name**: Каноническое название показателя (опционально)
    - **unit**: Единица измерения (опционально)
    - **date**: Дата добавления информации (опционально)
    - **target_level_min**: Минимальное целевое значение (опционально)
    - **target_level_max**: Максимальное целевое значение (опционально)
    
    Поле target_reached вычисляется автоматически по тем же правилам, как и для других показателей.
    
    Возвращает созданную запись об образе жизни с присвоенным ID.
    """
    repository = LifestyleInfoRepository(session)
    return await repository.create(data.model_dump())


@lifestyle_router.put("/{id}", response_model=LifestyleInfo, summary="Обновить запись об образе жизни")
async def update_lifestyle_info(id: int, data: LifestyleInfoCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующей записи об образе жизни.
    
    - **id**: Уникальный идентификатор записи для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленную запись об образе жизни, если она найдена, иначе выдает ошибку 404.
    """
    repository = LifestyleInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись об образе жизни с ID {id} не найдена"
        )
    return await repository.update(id, data.model_dump())


@lifestyle_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить запись об образе жизни")
async def delete_lifestyle_info(id: int, session: AsyncSession = Depends(get_session)):
    """
    Удаление записи об образе жизни.
    
    - **id**: Уникальный идентификатор записи для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = LifestyleInfoRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись об образе жизни с ID {id} не найдена"
        ) 