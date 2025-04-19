from typing import List
from pydantic import BaseModel, Field


class SymptomsList(BaseModel):
    symptoms: List[str] = Field(description="Список симптомов для диагностики")


class DiagnosticMethod(BaseModel):
    prediction: List[str] = Field(description="Результаты предсказания заболеваний")
    info: str = Field(description="Информация о методе предсказания")
    date: str = Field(description="Дата предсказания в формате ДД.ММ.ГГГГ")


class PredictionResponse(BaseModel):
    ml: DiagnosticMethod = Field(description="Результаты предсказания с использованием машинного обучения")
    ontology: DiagnosticMethod = Field(description="Результаты предсказания с использованием онтологии") 