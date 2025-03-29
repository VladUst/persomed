from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.health_indicators.session import get_session
from src.schemas.health_indicators import GeneralInfo, GeneralInfoCreate
from src.repositories.health_indicators import GeneralInfoRepository


# Создаем роутер для общей информации о здоровье
general_router = APIRouter(
    prefix="/general",
    tags=["Общая информация о здоровье"]
)


@general_router.get("/", response_model=List[GeneralInfo], summary="Получить всю базовую информацию о здоровье")
async def get_all_general_info(session: AsyncSession = Depends(get_session)):
    """
    Получение всех записей базовой информации о здоровье.
    
    Возвращает список всех записей базовой информации о здоровье.
    """
    repository = GeneralInfoRepository(session)
    return await repository.get_all()


@general_router.get("/{id}", response_model=GeneralInfo, summary="Получить базовую информацию о здоровье по ID")
async def get_general_info(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретной записи базовой информации о здоровье по её ID.
    
    - **id**: Уникальный идентификатор записи базовой информации о здоровье
    
    Возвращает запись базовой информации о здоровье, если она найдена, иначе выдает ошибку 404.
    """
    repository = GeneralInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Базовая информация с ID {id} не найдена"
        )
    return item


@general_router.post("/", response_model=GeneralInfo, status_code=status.HTTP_201_CREATED, summary="Создать общий показатель здоровья")
async def create_general_info(
    data: GeneralInfoCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание нового общего показателя здоровья.
    
    - **name**: Название показателя (обязательно)
    - **value**: Значение показателя (обязательно)
    - **canonical_name**: Каноническое название показателя (опционально)
    - **unit**: Единица измерения (опционально)
    - **date**: Дата измерения (опционально)
    - **target_level_min**: Минимальное целевое значение (опционально)
    - **target_level_max**: Максимальное целевое значение (опционально)
    
    Поле target_reached вычисляется автоматически:
    - Если target_level_min и target_level_max указаны и value можно преобразовать в число:
      - True, если value в пределах [target_level_min, target_level_max]
      - False, если value вне пределов
    - Если target_level_min или target_level_max не указаны или value нельзя преобразовать в число:
      - target_reached не устанавливается
    
    Возвращает созданный показатель здоровья с присвоенным ID.
    """
    repository = GeneralInfoRepository(session)
    return await repository.create(data.model_dump())


@general_router.put("/{id}", response_model=GeneralInfo, summary="Обновить базовую информацию о здоровье")
async def update_general_info(id: int, data: GeneralInfoCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующей записи базовой информации о здоровье.
    
    - **id**: Уникальный идентификатор записи для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленную запись базовой информации о здоровье, если она найдена, иначе выдает ошибку 404.
    """
    repository = GeneralInfoRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Базовая информация с ID {id} не найдена"
        )
    return await repository.update(id, data.model_dump())


@general_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить базовую информацию о здоровье")
async def delete_general_info(id: int, session: AsyncSession = Depends(get_session)):
    """
    Удаление записи базовой информации о здоровье.
    
    - **id**: Уникальный идентификатор записи для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = GeneralInfoRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Базовая информация с ID {id} не найдена"
        ) 