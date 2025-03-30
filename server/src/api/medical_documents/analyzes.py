from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.medical_documents.session import get_session
from src.schemas.medical_documents import AnalyzesDoc, AnalyzesDocCreate
from src.repositories.medical_documents import AnalyzesDocRepository


# Создаем роутер для документов по анализам
analyzes_router = APIRouter(
    prefix="/analyzes",
    tags=["Лабораторные и диагностические исследования"]
)


@analyzes_router.get("/", response_model=List[AnalyzesDoc], summary="Получить все документы анализов")
async def get_all_analyzes_docs(session: AsyncSession = Depends(get_session)):
    """
    Получение всех документов анализов.
    
    Возвращает список всех документов анализов.
    """
    repository = AnalyzesDocRepository(session)
    return await repository.get_all()


@analyzes_router.get("/{id}", response_model=AnalyzesDoc, summary="Получить документ анализа по ID")
async def get_analyzes_doc(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретного документа анализа по его ID.
    
    - **id**: Уникальный идентификатор документа анализа
    
    Возвращает документ анализа, если он найден, иначе выдает ошибку 404.
    """
    repository = AnalyzesDocRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ анализа с ID {id} не найден"
        )
    return item


@analyzes_router.post("/", response_model=AnalyzesDoc, status_code=status.HTTP_201_CREATED, summary="Создать документ с результатами анализов")
async def create_analyzes_doc(
    data: AnalyzesDocCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание нового документа анализа.
    
    - **name**: Название документа
    - **type**: Тип документа
    - **date**: Дата документа
    
    Возвращает созданный документ анализа с присвоенным ID.
    """
    repository = AnalyzesDocRepository(session)
    return await repository.create(data.model_dump())


@analyzes_router.put("/{id}", response_model=AnalyzesDoc, summary="Обновить документ анализа")
async def update_analyzes_doc(id: int, data: AnalyzesDocCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующего документа анализа.
    
    - **id**: Уникальный идентификатор документа для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленный документ анализа, если он найден, иначе выдает ошибку 404.
    """
    repository = AnalyzesDocRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ анализа с ID {id} не найден"
        )
    return await repository.update(id, data.model_dump())


@analyzes_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить документ анализа")
async def delete_analyzes_doc(id: int, session: AsyncSession = Depends(get_session)):
    """
    Удаление документа анализа.
    
    - **id**: Уникальный идентификатор документа для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = AnalyzesDocRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ анализа с ID {id} не найден"
        ) 