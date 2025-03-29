from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.health_indicators.session import get_session
from src.schemas.health_indicators import FamilyHistoryInfo, FamilyHistoryInfoCreate
from src.repositories.health_indicators import FamilyHistoryInfoRepository


# Создаем роутер для семейного анамнеза
family_history_router = APIRouter(
    prefix="/family-history",
    tags=["Семейный анамнез"]
)


@family_history_router.get("/", response_model=List[FamilyHistoryInfo], summary="Получить всю информацию о семейном анамнезе")
async def get_all_family_history_info(session: AsyncSession = Depends(get_session)):
    """
    Получение всех записей о семейном анамнезе.
    
    Возвращает список всех записей о семейном анамнезе.
    """
    repository = FamilyHistoryInfoRepository(session)
    return await repository.get_all()


@family_history_router.get("/{id}", response_model=FamilyHistoryInfo, summary="Получить информацию о семейном анамнезе по ID")
async def get_family_history_info(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретной записи о семейном анамнезе по её ID.
    
    - **id**: Уникальный идентификатор записи о семейном анамнезе
    
    Возвращает запись о семейном анамнезе, если она найдена, иначе выдает ошибку 404.
    """
    repository = FamilyHistoryInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись о семейном анамнезе с ID {id} не найдена"
        )
    return item


@family_history_router.post("/", response_model=FamilyHistoryInfo, status_code=status.HTTP_201_CREATED, summary="Создать информацию о семейном анамнезе")
async def create_family_history_info(
    data: FamilyHistoryInfoCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание новой записи о семейном анамнезе.
    
    - **name**: Название заболевания (обязательно)
    - **value**: У кого из родственников (обязательно)
    - **canonical_name**: Каноническое название заболевания (опционально)
    - **unit**: Единица измерения (опционально)
    - **date**: Дата добавления информации (опционально)
    - **target_level_min**: Минимальное целевое значение (опционально)
    - **target_level_max**: Максимальное целевое значение (опционально)
    
    Поле target_reached вычисляется автоматически по тем же правилам, как и для других показателей.
    
    Возвращает созданную запись о семейном анамнезе с присвоенным ID.
    """
    repository = FamilyHistoryInfoRepository(session)
    return await repository.create(data.model_dump())


@family_history_router.put("/{id}", response_model=FamilyHistoryInfo, summary="Обновить запись о семейном анамнезе")
async def update_family_history_info(id: int, data: FamilyHistoryInfoCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующей записи о семейном анамнезе.
    
    - **id**: Уникальный идентификатор записи для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленную запись о семейном анамнезе, если она найдена, иначе выдает ошибку 404.
    """
    repository = FamilyHistoryInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись о семейном анамнезе с ID {id} не найдена"
        )
    return await repository.update(id, data.model_dump())


@family_history_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить запись о семейном анамнезе")
async def delete_family_history_info(id: int, session: AsyncSession = Depends(get_session)):
    """
    Удаление записи о семейном анамнезе.
    
    - **id**: Уникальный идентификатор записи для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = FamilyHistoryInfoRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись о семейном анамнезе с ID {id} не найдена"
        ) 