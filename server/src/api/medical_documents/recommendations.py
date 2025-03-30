from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.medical_documents.session import get_session
from src.schemas.medical_documents import RecommendationsDoc, RecommendationsDocCreate
from src.repositories.medical_documents import RecommendationsDocRepository


# Создаем роутер для рекомендаций и назначений
recommendations_router = APIRouter(
    prefix="/recommendations",
    tags=["Рекомендации и назначения врачей"]
)


@recommendations_router.get("/", response_model=List[RecommendationsDoc], summary="Получить все документы рекомендаций")
async def get_all_recommendations_docs(session: AsyncSession = Depends(get_session)):
    """
    Получение всех документов рекомендаций и назначений.
    
    Возвращает список всех документов рекомендаций и назначений.
    """
    repository = RecommendationsDocRepository(session)
    return await repository.get_all()


@recommendations_router.get("/{id}", response_model=RecommendationsDoc, summary="Получить документ рекомендаций по ID")
async def get_recommendations_doc(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретного документа рекомендаций по его ID.
    
    - **id**: Уникальный идентификатор документа рекомендаций
    
    Возвращает документ рекомендаций, если он найден, иначе выдает ошибку 404.
    """
    repository = RecommendationsDocRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ рекомендаций с ID {id} не найден"
        )
    return item


@recommendations_router.post("/", response_model=RecommendationsDoc, status_code=status.HTTP_201_CREATED, summary="Создать документ с рекомендациями")
async def create_recommendations_doc(
    data: RecommendationsDocCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание нового документа рекомендаций.
    
    - **name**: Название документа
    - **type**: Тип документа
    - **date**: Дата документа
    - **specialty**: Специальность врача
    
    Возвращает созданный документ рекомендаций с присвоенным ID.
    """
    repository = RecommendationsDocRepository(session)
    return await repository.create(data.model_dump())


@recommendations_router.put("/{id}", response_model=RecommendationsDoc, summary="Обновить документ рекомендаций")
async def update_recommendations_doc(id: int, data: RecommendationsDocCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующего документа рекомендаций.
    
    - **id**: Уникальный идентификатор документа для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленный документ рекомендаций, если он найден, иначе выдает ошибку 404.
    """
    repository = RecommendationsDocRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ рекомендаций с ID {id} не найден"
        )
    return await repository.update(id, data.model_dump())


@recommendations_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить документ рекомендаций")
async def delete_recommendations_doc(id: int, session: AsyncSession = Depends(get_session)):
    """
    Удаление документа рекомендаций.
    
    - **id**: Уникальный идентификатор документа для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = RecommendationsDocRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ рекомендаций с ID {id} не найден"
        ) 