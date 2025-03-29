from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.health_indicators.session import get_session
from src.schemas.health_indicators import AllergiesInfo, AllergiesInfoCreate
from src.repositories.health_indicators import AllergiesInfoRepository


# Создаем роутер для аллергий
allergies_router = APIRouter(
    prefix="/allergies",
    tags=["Аллергии и непереносимости"]
)


@allergies_router.get("/", response_model=List[AllergiesInfo], summary="Получить всю информацию об аллергиях")
async def get_all_allergies_info(session: AsyncSession = Depends(get_session)):
    """
    Получение всех записей об аллергиях.
    
    Возвращает список всех записей об аллергиях.
    """
    repository = AllergiesInfoRepository(session)
    return await repository.get_all()


@allergies_router.get("/{id}", response_model=AllergiesInfo, summary="Получить информацию об аллергии по ID")
async def get_allergies_info(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретной записи об аллергии по её ID.
    
    - **id**: Уникальный идентификатор записи об аллергии
    
    Возвращает запись об аллергии, если она найдена, иначе выдает ошибку 404.
    """
    repository = AllergiesInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись об аллергии с ID {id} не найдена"
        )
    return item


@allergies_router.post("/", response_model=AllergiesInfo, status_code=status.HTTP_201_CREATED, summary="Создать информацию об аллергии")
async def create_allergies_info(
    data: AllergiesInfoCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание новой записи об аллергии.
    
    - **name**: Название аллергии (обязательно)
    - **value**: Тяжесть реакции (обязательно)
    - **canonical_name**: Каноническое название аллергии (опционально)
    - **unit**: Единица измерения (опционально)
    - **date**: Дата выявления (опционально)
    - **target_level_min**: Минимальное целевое значение (опционально)
    - **target_level_max**: Максимальное целевое значение (опционально)
    
    Поле target_reached вычисляется автоматически по тем же правилам, как и для других показателей.
    
    Возвращает созданную запись об аллергии с присвоенным ID.
    """
    repository = AllergiesInfoRepository(session)
    return await repository.create(data.model_dump())


@allergies_router.put("/{id}", response_model=AllergiesInfo, summary="Обновить запись об аллергии")
async def update_allergies_info(id: int, data: AllergiesInfoCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующей записи об аллергии.
    
    - **id**: Уникальный идентификатор записи для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленную запись об аллергии, если она найдена, иначе выдает ошибку 404.
    """
    repository = AllergiesInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись об аллергии с ID {id} не найдена"
        )
    return await repository.update(id, data.model_dump())


@allergies_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить запись об аллергии")
async def delete_allergies_info(id: int, session: AsyncSession = Depends(get_session)):
    """
    Удаление записи об аллергии.
    
    - **id**: Уникальный идентификатор записи для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = AllergiesInfoRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись об аллергии с ID {id} не найдена"
        ) 