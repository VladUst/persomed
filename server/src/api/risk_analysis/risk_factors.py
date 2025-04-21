from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.risk_analysis.session import get_session
from src.schemas.risk_analysis import RiskAnalysisResponse
from src.services.risk_analysis import get_risk_factors

# Создаем роутер для факторов риска
router = APIRouter(
    tags=["Анализ факторов риска"]
)


@router.get(
    "/risk-factors", 
    response_model=RiskAnalysisResponse, 
    status_code=status.HTTP_200_OK, 
    summary="Получить факторы риска",
    responses={
        200: {
            "description": "Успешный ответ с факторами риска",
            "content": {
                "application/json": {
                    "example": {
                        "low_level": {
                            "info": "Пониженный уровень у показателей: Гемоглобин, Лейкоциты",
                            "source": "Сервис анализа отклонений показателей от норм",
                            "date": "26.07.2023"
                        },
                        "high_level": {
                            "info": "Повышенный уровень у показателей: Холестерин, Глюкоза",
                            "source": "Сервис анализа отклонений показателей от норм",
                            "date": "26.07.2023"
                        },
                        "chronical": {
                            "info": "Хронические заболевания: Бронхиальная астма, Гипертония",
                            "source": "Сервис анализа хронических заболеваний",
                            "date": "26.07.2023"
                        }
                    }
                }
            }
        }
    }
)
async def get_user_risk_factors(session: AsyncSession = Depends(get_session)):
    """
    Анализ факторов риска пациента на основе показателей здоровья и хронических заболеваний.
    
    Метод выполняет три вида анализа:
    1. Показатели здоровья с пониженным уровнем
    2. Показатели здоровья с повышенным уровнем
    3. Хронические заболевания из истории болезней пациента
    
    Выходные параметры:
    - **low_level**: Информация о показателях с пониженным уровнем
      - info: Текстовое описание показателей с пониженным уровнем
      - source: Источник информации
      - date: Дата анализа
    - **high_level**: Информация о показателях с повышенным уровнем
      - info: Текстовое описание показателей с повышенным уровнем
      - source: Источник информации
      - date: Дата анализа
    - **chronical**: Информация о хронических заболеваниях
      - info: Текстовое описание хронических заболеваний
      - source: Источник информации
      - date: Дата анализа
    """
    # Получаем факторы риска из сервиса
    risk_factors = await get_risk_factors(session)
    
    return risk_factors 