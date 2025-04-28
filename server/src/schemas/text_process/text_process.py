from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class MedicalTextRequest(BaseModel):
    """
    Request schema for processing medical text.
    """
    text: str = Field(
        description="Медицинский текст для обработки и извлечения именованных сущностей"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Пациент имеет диагноз хроническая обструктивная болезнь легких и принимает будесонид ингаляционно."
            }
        }


class ICD10Entry(BaseModel):
    chapter: str = Field(description="Код МКБ-10")
    name: str = Field(description="Название диагноза по МКБ-10")


class NamedEntity(BaseModel):
    """
    Schema for a named entity extracted from medical text.
    """
    cui: str = Field(
        description="Концептуальный уникальный идентификатор (CUI) сущности в UMLS"
    )
    type_ids: List[str] = Field(
        description="Тип уникального идентификатора (TUI) сущности в UMLS",
        default_factory=list
    )
    types: List[str] = Field(
        description="Типы сущности в UMLS",
        default_factory=list
    )
    name: str = Field(
        description="Стандартизированное имя сущности"
    )
    definition: str = Field(
        description="Определение сущности из UMLS",
        default=""
    )
    icd10: List[ICD10Entry] = Field(
        description="Коды по Международной классификации болезней (МКБ)",
        default_factory=list
    )
    start_index: int = Field(
        description="Индекс начала сущности в исходном тексте"
    )
    end_index: int = Field(
        description="Индекс конца сущности в исходном тексте"
    )
    source_text: str = Field(
        description="Исходный текст сущности в документе"
    )
    confidence: float = Field(
        description="Уровень уверенности модели в обнаружении сущности (от 0 до 1)"
    )


class TextProcessingResponse(BaseModel):
    """
    Response schema for the text processing API.
    """
    entities: List[NamedEntity] = Field(
        description="Список извлеченных именованных сущностей",
        default_factory=list
    )
    count: int = Field(
        description="Общее количество найденных сущностей"
    ) 