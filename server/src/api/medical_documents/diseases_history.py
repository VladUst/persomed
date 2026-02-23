from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_depends import get_async_db
from src.schemas.medical_documents import (
    DiseasesHistoryDoc, DiseasesHistoryDocCreate,
    DiseasesHistoryDocDetails, DiseasesHistoryDocDetailsCreate,
    DiseasesHistoryDocWithDetails
)
from src.repositories.medical_documents import (
    DiseasesHistoryDocRepository,
    DiseasesHistoryDocDetailsRepository
)


# Создаем роутер для истории болезней
diseases_history_router = APIRouter(
    prefix="/diseases-history",
    tags=["История болезней"]
)


@diseases_history_router.get("/", response_model=List[DiseasesHistoryDocWithDetails], summary="Получить все документы истории болезней")
async def get_all_diseases_history_docs(db: AsyncSession = Depends(get_async_db)):
    """
    Получение всех документов истории болезней с их деталями (если доступны).
    
    Возвращает список всех документов истории болезней.
    """
    repository = DiseasesHistoryDocRepository(db)
    return await repository.get_all_with_details()


@diseases_history_router.get("/{id}", response_model=DiseasesHistoryDocWithDetails, summary="Получить документ истории болезни по ID")
async def get_diseases_history_doc(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Получение конкретного документа истории болезни по его ID с деталями (если доступны).
    
    - **id**: Уникальный идентификатор документа истории болезни
    
    Возвращает документ истории болезни, если он найден, иначе выдает ошибку 404.
    """
    repository = DiseasesHistoryDocRepository(db)
    item = await repository.get_by_id_with_details(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ истории болезни с ID {id} не найден"
        )
    return item


@diseases_history_router.post("/", response_model=DiseasesHistoryDoc, status_code=status.HTTP_201_CREATED, summary="Создать документ с историей болезни")
async def create_diseases_history_doc(
    data: DiseasesHistoryDocCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Создание нового документа истории болезни.
    
    - **name**: Название документа
    - **type**: Тип документа
    - **date**: Дата документа
    - **icd_code**: Код по МКБ
    
    Возвращает созданный документ истории болезни с присвоенным ID.
    """
    repository = DiseasesHistoryDocRepository(db)
    return await repository.create(data.model_dump())


@diseases_history_router.put("/{id}", response_model=DiseasesHistoryDoc, summary="Обновить документ истории болезни")
async def update_diseases_history_doc(id: int, data: DiseasesHistoryDocCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Обновление существующего документа истории болезни.
    
    - **id**: Уникальный идентификатор документа для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленный документ истории болезни, если он найден, иначе выдает ошибку 404.
    """
    repository = DiseasesHistoryDocRepository(db)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ истории болезни с ID {id} не найден"
        )
    return await repository.update(id, data.model_dump())


@diseases_history_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить документ истории болезни")
async def delete_diseases_history_doc(id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Удаление документа истории болезни.
    
    - **id**: Уникальный идентификатор документа для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = DiseasesHistoryDocRepository(db)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ истории болезни с ID {id} не найден"
        )


# Diseases History Document Details endpoints
@diseases_history_router.get("/{document_id}/details", response_model=DiseasesHistoryDocDetails, summary="Получить детали документа истории болезни")
async def get_diseases_history_doc_details(document_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Получение деталей для конкретного документа истории болезни.
    
    - **document_id**: ID документа истории болезни
    
    Возвращает детали документа истории болезни, если они найдены, иначе выдает ошибку 404.
    """
    repository = DiseasesHistoryDocDetailsRepository(db)
    item = await repository.get_by_document_id(document_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Детали для документа истории болезни с ID {document_id} не найдены"
        )
    return item


@diseases_history_router.post("/{document_id}/details", response_model=DiseasesHistoryDocDetails, status_code=status.HTTP_201_CREATED, summary="Добавить детали к истории болезни")
async def add_diseases_history_details(
    document_id: int,
    data: DiseasesHistoryDocDetailsCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Создание деталей для документа истории болезни.
    
    - **document_id**: ID документа истории болезни
    - **title**: Заголовок
    - **meta**: Метаинформация
      - **icd_code**: Код по МКБ
      - **diagnosis_date**: Дата диагноза
      - **doctor**: ФИО врача
      - **specialty**: Специальность врача
      - **nosology**: Название заболевания
      - **disease_type**: Тип заболевания
      - **clinic_name**: Название клиники
    - **sections**: Разделы документа
      - **anamnesis**: Анамнез (обязательное поле)
      - **clinical_findings**: Клинические находки (необязательное поле)
      - **diagnosis**: Диагноз (необязательное поле)
      - **treatment_plan**: План лечения (необязательное поле)
      - **conclusion**: Заключение (необязательное поле)
    
    Возвращает созданные детали документа истории болезни с присвоенным ID.
    """
    # Проверяем, существует ли документ
    doc_repository = DiseasesHistoryDocRepository(db)
    document = await doc_repository.get_by_id(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ истории болезни с ID {document_id} не найден"
        )
    
    # Проверяем, не существуют ли уже детали
    details_repository = DiseasesHistoryDocDetailsRepository(db)
    existing_details = await details_repository.get_by_document_id(document_id)
    if existing_details:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Детали для документа истории болезни с ID {document_id} уже существуют"
        )
    
    # Преобразуем вложенную структуру в плоскую для БД
    data_dict = {
        "id": document_id,  # Важно! id должен совпадать с document_id
        "document_id": document_id,
        "title": data.title,
        # Метаданные
        "icd_code": data.meta.icd_code,
        "diagnosis_date": data.meta.diagnosis_date,
        "doctor": data.meta.doctor,
        "specialty": data.meta.specialty,
        "nosology": data.meta.nosology,
        "disease_type": data.meta.disease_type,
        "clinic_name": data.meta.clinic_name,
        # Разделы
        "anamnesis": data.sections.anamnesis,
        "clinical_findings": data.sections.clinical_findings,
        "diagnosis": data.sections.diagnosis,
        "treatment_plan": data.sections.treatment_plan,
        "conclusion": data.sections.conclusion
    }
    
    return await details_repository.create(data_dict)


@diseases_history_router.put("/{document_id}/details", response_model=DiseasesHistoryDocDetails, summary="Обновить детали документа истории болезни")
async def update_diseases_history_doc_details(document_id: int, data: DiseasesHistoryDocDetailsCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Обновление деталей для документа истории болезни.
    
    - **document_id**: ID документа истории болезни
    - **data**: Обновленные данные деталей документа
      - **sections**: В разделах только поле "anamnesis" является обязательным
    
    Возвращает обновленные детали документа истории болезни, если они найдены, иначе выдает ошибку 404.
    """
    repository = DiseasesHistoryDocDetailsRepository(db)
    item = await repository.get_by_document_id(document_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Детали для документа истории болезни с ID {document_id} не найдены"
        )
    
    # Преобразуем вложенную структуру в плоскую для БД
    update_data = {
        "id": document_id,  # Важно! id должен совпадать с document_id
        "document_id": document_id,
        "title": data.title,
        # Метаданные
        "icd_code": data.meta.icd_code,
        "diagnosis_date": data.meta.diagnosis_date,
        "doctor": data.meta.doctor,
        "specialty": data.meta.specialty,
        "nosology": data.meta.nosology,
        "disease_type": data.meta.disease_type,
        "clinic_name": data.meta.clinic_name,
        # Разделы
        "anamnesis": data.sections.anamnesis,
        "clinical_findings": data.sections.clinical_findings,
        "diagnosis": data.sections.diagnosis,
        "treatment_plan": data.sections.treatment_plan,
        "conclusion": data.sections.conclusion
    }
    
    return await repository.update(item.id, update_data)


@diseases_history_router.delete("/{document_id}/details", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить детали документа истории болезни")
async def delete_diseases_history_doc_details(document_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Удаление деталей для документа истории болезни.
    
    - **document_id**: ID документа истории болезни
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = DiseasesHistoryDocDetailsRepository(db)
    item = await repository.get_by_document_id(document_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Детали для документа истории болезни с ID {document_id} не найдены"
        )
    
    success = await repository.delete(item.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить детали документа истории болезни"
        ) 