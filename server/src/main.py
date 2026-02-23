from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database import create_tables, delete_tables
from src.api import router


@asynccontextmanager
async def lifespan(app: FastAPI): 
    """ await delete_tables()
    print("База очищена") """
    await create_tables() 
    yield


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
    lifespan=lifespan
)

app.include_router(router)