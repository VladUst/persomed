from typing import List, Optional
from pydantic import BaseModel, Field


class Symptom(BaseModel):
    name: str = Field(description="Название симптома")
    source: str = Field(description="Источник информации о симптоме")
    date: str = Field(description="Дата фиксации симптома")


class Disease(BaseModel):
    id: int = Field(description="Идентификатор заболевания")
    name: str = Field(description="Название заболевания")
    type: str = Field(description="Тип заболевания")
    date: str = Field(description="Дата заболевания")
    icd_code: str = Field(description="Код заболевания по МКБ-10")


class Rate(BaseModel):
    name: str = Field(description="Категория заболеваний")
    rate: str = Field(description="Оценка риска (Высокие, Средние, Низкие, Неизвестно)")
    source: str = Field(description="Источник оценки")
    date: str = Field(description="Дата оценки")


class Suspicion(BaseModel):
    name: str = Field(description="Название подозреваемого заболевания")
    date: str = Field(description="Дата подозрения")
    icd: str = Field(description="Код заболевания по МКБ-10")


class Risk(BaseModel):
    info: str = Field(description="Информация о факторе риска")
    source: str = Field(description="Источник данных о факторе риска")
    date: str = Field(description="Дата получения информации")


class Drug(BaseModel):
    name: str = Field(description="Название препарата")
    dosage: str = Field(description="Дозировка препарата")
    date: str = Field(description="Дата назначения")


class Recommendation(BaseModel):
    name: str = Field(description="Текст рекомендации")
    source: str = Field(description="Источник рекомендации")
    date: str = Field(description="Дата рекомендации")


class PatientStatus(BaseModel):
    symptoms: List[Symptom] = Field(description="Симптомы пациента")
    diseases: List[Disease] = Field(description="Заболевания пациента")
    rates: List[Rate] = Field(description="Оценки рисков заболеваний по категориям")
    suspicions: List[Suspicion] = Field(description="Подозрения на заболевания")
    risks: dict = Field(description="Факторы риска")
    drugs: List[Drug] = Field(description="Назначенные препараты")
    recommendations: List[Recommendation] = Field(description="Рекомендации")


class PatientStatusResponse(BaseModel):
    status: PatientStatus = Field(description="Полный статус пациента") 