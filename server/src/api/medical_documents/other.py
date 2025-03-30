from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.medical_documents.session import get_session
from src.schemas.medical_documents import OtherDoc, OtherDocCreate
from src.repositories.medical_documents import OtherDocRepository


# Создаем роутер для прочих документов
other_router = APIRouter(
    prefix="/other",
    tags=["Другие документы"]
)


@other_router.get("/", response_model=List[OtherDoc], summary="Получить все прочие документы")
async def get_all_other_docs(session: AsyncSession = Depends(get_session)):
    """
    Получение всех прочих медицинских документов.
    
    Возвращает список всех прочих медицинских документов.
    """
    repository = OtherDocRepository(session)
    return await repository.get_all()


@other_router.get("/{id}", response_model=OtherDoc, summary="Получить прочий документ по ID")
async def get_other_doc(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретного прочего медицинского документа по его ID.
    
    - **id**: Уникальный идентификатор прочего документа
    
    Возвращает прочий документ, если он найден, иначе выдает ошибку 404.
    """
    repository = OtherDocRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Прочий документ с ID {id} не найден"
        )
    return item


@other_router.post("/", response_model=OtherDoc, status_code=status.HTTP_201_CREATED, summary="Создать прочий документ")
async def create_other_doc(
    data: OtherDocCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание нового прочего медицинского документа.
    
    - **name**: Название документа
    - **type**: Тип документа
    - **date**: Дата документа
    
    Возвращает созданный прочий документ с присвоенным ID.
    """
    repository = OtherDocRepository(session)
    return await repository.create(data.model_dump())


@other_router.put("/{id}", response_model=OtherDoc, summary="Обновить прочий документ")
async def update_other_doc(id: int, data: OtherDocCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующего прочего медицинского документа.
    
    - **id**: Уникальный идентификатор документа для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленный прочий документ, если он найден, иначе выдает ошибку 404.
    """
    repository = OtherDocRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Прочий документ с ID {id} не найден"
        )
    return await repository.update(id, data.model_dump())


@other_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить прочий документ")
async def delete_other_doc(id: int, session: AsyncSession = Depends(get_session)):
    """
    Удаление прочего медицинского документа.
    
    - **id**: Уникальный идентификатор документа для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = OtherDocRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Прочий документ с ID {id} не найден"
        ) 