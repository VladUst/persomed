from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_depends import get_async_db
from src.schemas.medical_documents import OtherDoc, OtherDocCreate
from src.repositories.medical_documents import OtherDocRepository

# Создаем роутер для прочих документов
other_router = APIRouter(
    prefix="/other",
    tags=["Другие документы"]
)

@other_router.get("/", response_model=List[OtherDoc], summary="Получить все прочие документы")
async def get_all_other_docs(db: AsyncSession = Depends(get_async_db)):
    """
    Получение всех прочих медицинских документов.
    
    Возвращает список всех прочих медицинских документов.
    """
    repository = OtherDocRepository(db)
    return await repository.get_all()


@other_router.get("/{id}", response_model=OtherDoc, summary="Получить документ по ID")
async def get_other_doc(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Получение конкретного прочего медицинского документа по его ID.
    
    - **id**: Уникальный идентификатор прочего документа
    
    Возвращает прочий документ, если он найден, иначе выдает ошибку 404.
    """
    repository = OtherDocRepository(db)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ с ID {id} не найден"
        )
    return item


@other_router.post("/", response_model=OtherDoc, status_code=status.HTTP_201_CREATED, summary="Создать документ")
async def create_other_doc(
    data: OtherDocCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Создание нового прочего медицинского документа.
    
    - **name**: Название документа
    - **type**: Тип документа
    - **date**: Дата документа
    
    Возвращает созданный прочий документ с присвоенным ID.
    """
    repository = OtherDocRepository(db)
    return await repository.create(data.model_dump())


@other_router.put("/{id}", response_model=OtherDoc, summary="Обновить документ")
async def update_other_doc(id: int, data: OtherDocCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Обновление существующего прочего медицинского документа.
    
    - **id**: Уникальный идентификатор документа для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленный прочий документ, если он найден, иначе выдает ошибку 404.
    """
    repository = OtherDocRepository(db)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ с ID {id} не найден"
        )
    return await repository.update(id, data.model_dump())


@other_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить документ")
async def delete_other_doc(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Удаление прочего медицинского документа.
    
    - **id**: Уникальный идентификатор документа для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = OtherDocRepository(db)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ с ID {id} не найден"
        ) 