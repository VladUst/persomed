import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import router
from src.api.genes import install_report_examples


app = FastAPI(
    title="Интеллектуальная персонализированная медицинская информационная система PersoMed",
    description="""
    API для работы с цифровым профилем пациента медицинской информационной системы.
    
    Цифровой профиль пациента содержит информацию о показателях здоровья пациента и медицинские документы.

    ### Показатели здоровья
    * Базовая информация
    * Лабораторные измерения
    * Прививки и профилактические мероприятия
    * Аллергии
    * Семейный анамнез
    * Образ жизни
    
    ### Медицинские документы
    * История болезней со списком диагнозов
    * Документы анализов 
    * Рекомендации и назначения врачей
    * Прочие документы
    """,
    version="1.0.0",
)

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "PERSOMED_CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(router)
install_report_examples(app)
