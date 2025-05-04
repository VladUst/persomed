from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.medical_documents.session import get_session
from src.schemas.medical_documents import (
    RecommendationsDoc, RecommendationsDocCreate,
    RecommendationsDocDetails, RecommendationsDocDetailsCreate,
    RecommendationsDocWithDetails
)
from src.repositories.medical_documents import (
    RecommendationsDocRepository,
    RecommendationsDocDetailsRepository
)


# Создаем роутер для рекомендаций и назначений
recommendations_router = APIRouter(
    prefix="/recommendations",
    tags=["Рекомендации и назначения врачей"]
)


@recommendations_router.get("/", response_model=List[RecommendationsDocWithDetails], summary="Получить все документы рекомендаций")
async def get_all_recommendations_docs(session: AsyncSession = Depends(get_session)):
    """
    Получение всех документов рекомендаций и назначений с их деталями (если доступны).
    
    Возвращает список всех документов рекомендаций и назначений.
    """
    repository = RecommendationsDocRepository(session)
    return await repository.get_all_with_details()


@recommendations_router.get("/{id}", response_model=RecommendationsDocWithDetails, summary="Получить документ рекомендаций по ID")
async def get_recommendations_doc(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретного документа рекомендаций по его ID с деталями (если доступны).
    
    - **id**: Уникальный идентификатор документа рекомендаций
    
    Возвращает документ рекомендаций, если он найден, иначе выдает ошибку 404.
    """
    repository = RecommendationsDocRepository(session)
    item = await repository.get_by_id_with_details(id)
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


# Recommendations Document Details endpoints
@recommendations_router.get("/{document_id}/details", response_model=RecommendationsDocDetails, summary="Получить детали документа рекомендаций")
async def get_recommendations_doc_details(document_id: int, session: AsyncSession = Depends(get_session)):
    """
    Получение деталей для конкретного документа рекомендаций.
    
    - **document_id**: ID документа рекомендаций
    
    Возвращает детали документа рекомендаций, если они найдены, иначе выдает ошибку 404.
    """
    repository = RecommendationsDocDetailsRepository(session)
    item = await repository.get_by_document_id(document_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Детали для документа рекомендаций с ID {document_id} не найдены"
        )
    return item


@recommendations_router.post("/{document_id}/details", response_model=RecommendationsDocDetails, status_code=status.HTTP_201_CREATED, summary="Добавить детали к рекомендациям")
async def add_recommendations_details(
    document_id: int,
    data: RecommendationsDocDetailsCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Создание деталей для документа рекомендаций.
    
    - **document_id**: ID документа рекомендаций
    - **title**: Заголовок
    - **meta**: Метаинформация
      - **icd_code**: Код по МКБ
      - **date**: Дата рекомендации
      - **doctor**: ФИО врача
      - **specialty**: Специальность врача
      - **type**: Тип рекомендации
      - **clinic_name**: Название клиники
    - **sections**: Разделы документа
      - **instructions**: Инструкции по применению рекомендаций
    
    Возвращает созданные детали документа рекомендаций с присвоенным ID.
    """
    # Проверяем, существует ли документ
    doc_repository = RecommendationsDocRepository(session)
    document = await doc_repository.get_by_id(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ рекомендаций с ID {document_id} не найден"
        )
    
    # Проверяем, не существуют ли уже детали
    details_repository = RecommendationsDocDetailsRepository(session)
    existing_details = await details_repository.get_by_document_id(document_id)
    if existing_details:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Детали для документа рекомендаций с ID {document_id} уже существуют"
        )
    
    # Преобразуем вложенную структуру в плоскую для БД
    data_dict = {
        "id": document_id,  # Важно! id должен совпадать с document_id
        "document_id": document_id,
        "title": data.title,
        # Метаданные
        "icd_code": data.meta.icd_code,
        "date": data.meta.date,
        "doctor": data.meta.doctor,
        "specialty": data.meta.specialty,
        "type": data.meta.type,
        "clinic_name": data.meta.clinic_name,
        # Разделы
        "instructions": data.sections.instructions
    }
    
    return await details_repository.create(data_dict)


@recommendations_router.put("/{document_id}/details", response_model=RecommendationsDocDetails, summary="Обновить детали документа рекомендаций")
async def update_recommendations_doc_details(document_id: int, data: RecommendationsDocDetailsCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление деталей для документа рекомендаций.
    
    - **document_id**: ID документа рекомендаций
    - **data**: Обновленные данные деталей документа
    
    Возвращает обновленные детали документа рекомендаций, если они найдены, иначе выдает ошибку 404.
    """
    repository = RecommendationsDocDetailsRepository(session)
    item = await repository.get_by_document_id(document_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Детали для документа рекомендаций с ID {document_id} не найдены"
        )
    
    # Преобразуем вложенную структуру в плоскую для БД
    update_data = {
        "id": document_id,  # Важно! id должен совпадать с document_id
        "document_id": document_id,
        "title": data.title,
        # Метаданные
        "icd_code": data.meta.icd_code,
        "date": data.meta.date,
        "doctor": data.meta.doctor,
        "specialty": data.meta.specialty,
        "type": data.meta.type,
        "clinic_name": data.meta.clinic_name,
        # Разделы
        "instructions": data.sections.instructions
    }
    
    return await repository.update(item.id, update_data)


@recommendations_router.delete("/{document_id}/details", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить детали документа рекомендаций")
async def delete_recommendations_doc_details(document_id: int, session: AsyncSession = Depends(get_session)):
    """
    Удаление деталей для документа рекомендаций.
    
    - **document_id**: ID документа рекомендаций
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = RecommendationsDocDetailsRepository(session)
    item = await repository.get_by_document_id(document_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Детали для документа рекомендаций с ID {document_id} не найдены"
        )
    
    success = await repository.delete(item.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить детали документа рекомендаций"
        ) 