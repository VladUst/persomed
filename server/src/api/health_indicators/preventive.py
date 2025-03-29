from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.health_indicators.session import get_session
from src.schemas.health_indicators import PreventiveInfo, PreventiveInfoCreate
from src.repositories.health_indicators import PreventiveInfoRepository


# Создаем роутер для прививок и профилактических мероприятий
preventive_router = APIRouter(
    prefix="/preventive",
    tags=["Вакцинации и профилактические мероприятия"]
)


@preventive_router.get("/", response_model=List[PreventiveInfo], summary="Получить всю информацию о прививках и профилактике")
async def get_all_preventive_info(session: AsyncSession = Depends(get_session)):
    """
    Получение всех записей о прививках и профилактических мероприятиях.
    
    Возвращает список всех записей о прививках и профилактических мероприятиях.
    """
    repository = PreventiveInfoRepository(session)
    return await repository.get_all()


@preventive_router.get("/{id}", response_model=PreventiveInfo, summary="Получить информацию о прививке по ID")
async def get_preventive_info(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретной записи о прививке/профилактике по её ID.
    
    - **id**: Уникальный идентификатор записи о прививке
    
    Возвращает запись о прививке/профилактике, если она найдена, иначе выдает ошибку 404.
    """
    repository = PreventiveInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись о прививке с ID {id} не найдена"
        )
    return item


@preventive_router.post("/", response_model=PreventiveInfo, status_code=status.HTTP_201_CREATED, summary="Создать профилактический показатель")
async def create_preventive_info(
    data: PreventiveInfoCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание нового профилактического показателя.
    
    - **name**: Название показателя (обязательно)
    - **value**: Значение показателя (обязательно)
    - **canonical_name**: Каноническое название показателя (опционально)
    - **unit**: Единица измерения (опционально)
    - **date**: Дата измерения (опционально)
    - **target_level_min**: Минимальное целевое значение (опционально)
    - **target_level_max**: Максимальное целевое значение (опционально)
    
    Поле target_reached вычисляется автоматически по тем же правилам, как и для других показателей.
    
    Возвращает созданный профилактический показатель с присвоенным ID.
    """
    repository = PreventiveInfoRepository(session)
    return await repository.create(data.model_dump())


@preventive_router.put("/{id}", response_model=PreventiveInfo, summary="Обновить запись о прививке/профилактике")
async def update_preventive_info(id: int, data: PreventiveInfoCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующей записи о прививке/профилактике.
    
    - **id**: Уникальный идентификатор записи для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленную запись о прививке/профилактике, если она найдена, иначе выдает ошибку 404.
    """
    repository = PreventiveInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись о прививке с ID {id} не найдена"
        )
    return await repository.update(id, data.model_dump())


@preventive_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить запись о прививке/профилактике")
async def delete_preventive_info(id: int, session: AsyncSession = Depends(get_session)):
    """
    Удаление записи о прививке/профилактике.
    
    - **id**: Уникальный идентификатор записи для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = PreventiveInfoRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись о прививке с ID {id} не найдена"
        ) 