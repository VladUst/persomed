from typing import List, Annotated, Type, TypeVar, Any
from fastapi import APIRouter, Depends, HTTPException, status, Form, Body
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from src.database import new_session
from src.schemas import (
    AnalyzesDoc, AnalyzesDocCreate,
    OtherDoc, OtherDocCreate,
    DiseasesHistoryDoc, DiseasesHistoryDocCreate,
    RecommendationsDoc, RecommendationsDocCreate,
    DiseasesHistoryDocDetails, DiseasesHistoryDocDetailsCreate,
    DiseasesHistoryDocWithDetails
)
from src.repositories import (
    AnalyzesDocRepository,
    OtherDocRepository,
    DiseasesHistoryDocRepository,
    RecommendationsDocRepository,
    DiseasesHistoryDocDetailsRepository
)


async def get_session():
    async with new_session() as session:
        yield session


# Создаем роутер для документов по анализам
analyzes_router = APIRouter(
    prefix="/analyzes",
    tags=["Лабораторные и диагностические исследования"]
)

# Создаем роутер для прочих документов
other_router = APIRouter(
    prefix="/other",
    tags=["Другие документы"]
)

# Создаем роутер для истории болезней
diseases_history_router = APIRouter(
    prefix="/diseases-history",
    tags=["История болезней"]
)

# Создаем роутер для рекомендаций и назначений
recommendations_router = APIRouter(
    prefix="/recommendations",
    tags=["Рекомендации и назначения врачей"]
)

# Объединяем все роутеры в один общий, сохраняя категоризацию
router = APIRouter(
    prefix="/medical-documents"
)


T = TypeVar('T', bound=BaseModel)

def form_dependency(model_class: Type[T]) -> Any:
    """
    Создает зависимость FastAPI для получения модели из form-data параметров.
    
    Это позволяет отображать поля модели как Form-параметры в Swagger UI.
    """
    fields = model_class.__annotations__
    
    def create_form(**kwargs):
        return model_class(**kwargs)
    
    # Получаем все поля модели и создаем Form-зависимости
    signature_params = {
        field_name: Depends(
            lambda field_name=field_name, field_type=field_type: Form(
                ...,
                description=f"Поле {field_name}"
            )
        )
        for field_name, field_type in fields.items()
    }
    
    # Добавляем зависимость с созданной сигнатурой
    return Depends(create_form)


# Analyzes Documents endpoints
@analyzes_router.get("/", response_model=List[AnalyzesDoc], summary="Получить все документы анализов")
async def get_all_analyzes_docs(session: AsyncSession = Depends(get_session)):
    """
    Получение всех документов анализов.
    
    Возвращает список всех документов анализов.
    """
    repository = AnalyzesDocRepository(session)
    return await repository.get_all()


@analyzes_router.get("/{id}", response_model=AnalyzesDoc, summary="Получить документ анализа по ID")
async def get_analyzes_doc(id: str, session: AsyncSession = Depends(get_session)):
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


@analyzes_router.post("/", response_model=AnalyzesDoc, status_code=status.HTTP_201_CREATED, summary="Создать документ анализа")
async def create_analyzes_doc(
    data: Annotated[AnalyzesDocCreate, Depends()],
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
async def update_analyzes_doc(id: str, data: AnalyzesDocCreate, session: AsyncSession = Depends(get_session)):
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
async def delete_analyzes_doc(id: str, session: AsyncSession = Depends(get_session)):
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


# Other Documents endpoints
@other_router.get("/", response_model=List[OtherDoc], summary="Получить все прочие документы")
async def get_all_other_docs(session: AsyncSession = Depends(get_session)):
    """
    Получение всех прочих медицинских документов.
    
    Возвращает список всех прочих медицинских документов.
    """
    repository = OtherDocRepository(session)
    return await repository.get_all()


@other_router.get("/{id}", response_model=OtherDoc, summary="Получить прочий документ по ID")
async def get_other_doc(id: str, session: AsyncSession = Depends(get_session)):
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
    data: Annotated[OtherDocCreate, Depends()],
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
async def update_other_doc(id: str, data: OtherDocCreate, session: AsyncSession = Depends(get_session)):
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
async def delete_other_doc(id: str, session: AsyncSession = Depends(get_session)):
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


# Diseases History Documents endpoints
@diseases_history_router.get("/", response_model=List[DiseasesHistoryDocWithDetails], summary="Получить все документы истории болезней")
async def get_all_diseases_history_docs(session: AsyncSession = Depends(get_session)):
    """
    Получение всех документов истории болезней с их деталями (если доступны).
    
    Возвращает список всех документов истории болезней.
    """
    repository = DiseasesHistoryDocRepository(session)
    return await repository.get_all_with_details()


@diseases_history_router.get("/{id}", response_model=DiseasesHistoryDocWithDetails, summary="Получить документ истории болезни по ID")
async def get_diseases_history_doc(id: str, session: AsyncSession = Depends(get_session)):
    """
    Получение конкретного документа истории болезни по его ID с деталями (если доступны).
    
    - **id**: Уникальный идентификатор документа истории болезни
    
    Возвращает документ истории болезни, если он найден, иначе выдает ошибку 404.
    """
    repository = DiseasesHistoryDocRepository(session)
    item = await repository.get_by_id_with_details(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ истории болезни с ID {id} не найден"
        )
    return item


@diseases_history_router.post("/", response_model=DiseasesHistoryDoc, status_code=status.HTTP_201_CREATED, summary="Создать документ истории болезни")
async def create_diseases_history_doc(
    data: Annotated[DiseasesHistoryDocCreate, Depends()],
    session: AsyncSession = Depends(get_session)
):
    """
    Создание нового документа истории болезни.
    
    - **name**: Название документа
    - **type**: Тип документа
    - **date**: Дата документа
    - **icd_code**: Код по МКБ
    
    Возвращает созданный документ истории болезни с присвоенным ID.
    """
    repository = DiseasesHistoryDocRepository(session)
    return await repository.create(data.model_dump())


@diseases_history_router.put("/{id}", response_model=DiseasesHistoryDoc, summary="Обновить документ истории болезни")
async def update_diseases_history_doc(id: str, data: DiseasesHistoryDocCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление существующего документа истории болезни.
    
    - **id**: Уникальный идентификатор документа для обновления
    - **data**: Обновленные данные
    
    Возвращает обновленный документ истории болезни, если он найден, иначе выдает ошибку 404.
    """
    repository = DiseasesHistoryDocRepository(session)
    item = await repository.get_by_id(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ истории болезни с ID {id} не найден"
        )
    return await repository.update(id, data.model_dump())


@diseases_history_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить документ истории болезни")
async def delete_diseases_history_doc(id: str, session: AsyncSession = Depends(get_session)):
    """
    Удаление документа истории болезни.
    
    - **id**: Уникальный идентификатор документа для удаления
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = DiseasesHistoryDocRepository(session)
    success = await repository.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ истории болезни с ID {id} не найден"
        )


# Diseases History Document Details endpoints
@diseases_history_router.get("/{document_id}/details", response_model=DiseasesHistoryDocDetails, summary="Получить детали документа истории болезни")
async def get_diseases_history_doc_details(document_id: str, session: AsyncSession = Depends(get_session)):
    """
    Получение деталей для конкретного документа истории болезни.
    
    - **document_id**: ID документа истории болезни
    
    Возвращает детали документа истории болезни, если они найдены, иначе выдает ошибку 404.
    """
    repository = DiseasesHistoryDocDetailsRepository(session)
    item = await repository.get_by_document_id(document_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Детали для документа истории болезни с ID {document_id} не найдены"
        )
    return item


@diseases_history_router.post("/details", response_model=DiseasesHistoryDocDetails, status_code=status.HTTP_201_CREATED, summary="Создать детали документа истории болезни")
async def create_diseases_history_doc_details(
    data: Annotated[DiseasesHistoryDocDetailsCreate, Depends()],
    session: AsyncSession = Depends(get_session)
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
      - **anamnesis**: Анамнез
      - **clinical_findings**: Клинические находки
      - **diagnosis**: Диагноз
      - **treatment_plan**: План лечения
      - **conclusion**: Заключение
    
    Возвращает созданные детали документа истории болезни с присвоенным ID.
    """
    # Проверяем, существует ли документ
    doc_repository = DiseasesHistoryDocRepository(session)
    document = await doc_repository.get_by_id(data.document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Документ истории болезни с ID {data.document_id} не найден"
        )
    
    # Проверяем, не существуют ли уже детали
    details_repository = DiseasesHistoryDocDetailsRepository(session)
    existing_details = await details_repository.get_by_document_id(data.document_id)
    if existing_details:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Детали для документа истории болезни с ID {data.document_id} уже существуют"
        )
    
    return await details_repository.create(data.model_dump())


@diseases_history_router.put("/{document_id}/details", response_model=DiseasesHistoryDocDetails, summary="Обновить детали документа истории болезни")
async def update_diseases_history_doc_details(document_id: str, data: DiseasesHistoryDocDetailsCreate, session: AsyncSession = Depends(get_session)):
    """
    Обновление деталей для документа истории болезни.
    
    - **document_id**: ID документа истории болезни
    - **data**: Обновленные данные деталей документа
    
    Возвращает обновленные детали документа истории болезни, если они найдены, иначе выдает ошибку 404.
    """
    repository = DiseasesHistoryDocDetailsRepository(session)
    item = await repository.get_by_document_id(document_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Детали для документа истории болезни с ID {document_id} не найдены"
        )
    
    # Обеспечиваем соответствие document_id
    update_data = data.model_dump()
    update_data["document_id"] = document_id
    
    return await repository.update(item.id, update_data)


@diseases_history_router.delete("/{document_id}/details", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить детали документа истории болезни")
async def delete_diseases_history_doc_details(document_id: str, session: AsyncSession = Depends(get_session)):
    """
    Удаление деталей для документа истории болезни.
    
    - **document_id**: ID документа истории болезни
    
    Возвращает статус 204 No Content при успешном удалении, иначе выдает ошибку 404.
    """
    repository = DiseasesHistoryDocDetailsRepository(session)
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


# Recommendations Documents endpoints
@recommendations_router.get("/", response_model=List[RecommendationsDoc], summary="Получить все документы рекомендаций")
async def get_all_recommendations_docs(session: AsyncSession = Depends(get_session)):
    """
    Получение всех документов рекомендаций и назначений.
    
    Возвращает список всех документов рекомендаций и назначений.
    """
    repository = RecommendationsDocRepository(session)
    return await repository.get_all()


@recommendations_router.get("/{id}", response_model=RecommendationsDoc, summary="Получить документ рекомендаций по ID")
async def get_recommendations_doc(id: str, session: AsyncSession = Depends(get_session)):
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


@recommendations_router.post("/", response_model=RecommendationsDoc, status_code=status.HTTP_201_CREATED, summary="Создать документ рекомендаций")
async def create_recommendations_doc(
    data: Annotated[RecommendationsDocCreate, Depends()],
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
async def update_recommendations_doc(id: str, data: RecommendationsDocCreate, session: AsyncSession = Depends(get_session)):
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
async def delete_recommendations_doc(id: str, session: AsyncSession = Depends(get_session)):
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

# Включаем все роутеры в основной роутер
router.include_router(analyzes_router)
router.include_router(other_router)
router.include_router(diseases_history_router)
router.include_router(recommendations_router) 