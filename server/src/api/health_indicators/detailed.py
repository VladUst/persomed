from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.health_indicators.session import get_session
from src.schemas.health_indicators import DetailedInfo, DetailedInfoCreate
from src.repositories.health_indicators import DetailedInfoRepository


# Создаем роутер для лабораторных измерений
detailed_router = APIRouter(
    prefix="/detailed",
    tags=["Лабораторные измерения"]
)


@detailed_router.get("/", response_model=List[DetailedInfo], summary="Получить все лабораторные измерения")
async def get_all_detailed_info(session: AsyncSession = Depends(get_session)):
    """
    Получение всех записей лабораторных измерений.
    
    Возвращает список всех записей лабораторных измерений.
    """
    repository = DetailedInfoRepository(session)
    return await repository.get_all()


@detailed_router.get("/{id}", response_model=DetailedInfo, summary="Получить лабораторное измерение по ID")
async def get_detailed_info(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретной записи лабораторного измерения по её ID.
    
    - **id**: Уникальный идентификатор лабораторного измерения
    
    Возвращает запись лабораторного измерения, если оно найдено, иначе выдает ошибку 404.
    """
    repository = DetailedInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Лабораторное измерение с ID {id} не найдено"
        )
    return item


@detailed_router.post("/", response_model=DetailedInfo, status_code=status.HTTP_201_CREATED, summary="Создать лабораторное измерение")
async def create_detailed_info(
    data: DetailedInfoCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание нового лабораторного измерения.
    
    - **name**: Название показателя (обязательно)
    - **value**: Числовое значение показателя (обязательно, float)
    - **canonical_name**: Каноническое название показателя (опционально)
    - **unit**: Единица измерения (опционально)
    - **date**: Дата измерения (опционально)
    - **target_level_min**: Минимальное целевое значение (опционально)
    - **target_level_max**: Максимальное целевое значение (опционально)
    
    Поле target_reached вычисляется автоматически:
    - Если target_level_min и target_level_max указаны:
      - True, если value в пределах [target_level_min, target_level_max]
      - False, если value вне пределов
    - Если target_level_min или target_level_max не указаны:
      - target_reached не устанавливается
    
    Возвращает созданное лабораторное измерение с присвоенным ID.
    """
    repository = DetailedInfoRepository(session)
    return await repository.create(data.model_dump())


@detailed_router.put("/{id}", response_model=DetailedInfo, summary="Обновить лабораторное измерение")
async def update_detailed_info(id: int, data: DetailedInfoCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующей записи лабораторного измерения.
    
    - **id**: Уникальный идентификатор записи для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленную запись лабораторного измерения, если она найдена, иначе выдает ошибку 404.
    """
    repository = DetailedInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Лабораторное измерение с ID {id} не найдено"
        )
    return await repository.update(id, data.model_dump())


@detailed_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить лабораторное измерение")
async def delete_detailed_info(id: int, session: AsyncSession = Depends(get_session)):
    """
    Удаление записи лабораторного измерения.
    
    - **id**: Уникальный идентификатор записи для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = DetailedInfoRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Лабораторное измерение с ID {id} не найдено"
        ) 