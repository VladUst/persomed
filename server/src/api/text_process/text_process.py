from fastapi import APIRouter, status, Body
from typing import List

from src.schemas.text_process import MedicalTextRequest, TextProcessingResponse, NamedEntity
from src.services.text_processing import process_medical_text

# Create router for entity extraction endpoints
router = APIRouter(
    tags=["Сервис обработки текстов"]
)


@router.post(
    "/entities",
    response_model=TextProcessingResponse,
    status_code=status.HTTP_200_OK,
    summary="Извлечь именованные медицинские сущности из текста" 
)
async def extract_entities(
    data: MedicalTextRequest = Body(
        ...,
        example={"text": "У пациента наблюдаются покашливание, хриплость и стридор."}
    )
):
    """
    Извлечение именованных медицинских сущностей из текста с помощью MedCAT.
    
    Метод анализирует медицинский текст и извлекает из него именованные сущности, такие как:
    - Заболевания
    - Симптомы
    - Лекарственные препараты
    - Анатомические структуры
    - Процедуры
    - Другие медицинские концепты
    
    Для каждой найденной сущности возвращается подробная информация:
    - CUI (Concept Unique Identifier) - уникальный идентификатор концепта в UMLS
    - TUI (Type Unique Identifier) - идентификаторы типов концепта в UMLS
    - Название сущности (стандартизированное)
    - Определение сущности (если доступно)
    - Код МКБ (если доступен)
    - Позиция в тексте
    - Исходный текст сущности
    - Уровень уверенности в распознавании
    
    Входные параметры:
    - **text**: Медицинский текст для анализа и извлечения сущностей
    - **language**: Язык текста ("en" или "ru"), по умолчанию "en"
    
    Выходные параметры:
    - **entities**: Список извлеченных именованных сущностей с их атрибутами
    - **count**: Общее количество найденных сущностей
    """
    # Process the text and extract entities
    entities = await process_medical_text(data.text, data.language)
    
    # Convert to Pydantic models
    entity_models = [NamedEntity(**entity) for entity in entities]
    
    # Create response
    response = TextProcessingResponse(
        entities=entity_models,
        count=len(entity_models)
    )
    
    return response 