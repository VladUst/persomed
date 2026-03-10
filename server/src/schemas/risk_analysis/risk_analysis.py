from pydantic import BaseModel, Field

class RiskFactorInfo(BaseModel):
    info: str = Field(..., description="Текстовое описание факторов риска")
    source: str = Field(..., description="Источник информации о факторах риска")
    date: str = Field(..., description="Дата анализа факторов риска")


class RiskAnalysisResponse(BaseModel):
    low_level: RiskFactorInfo = Field(
        ..., 
        description="Информация о показателях с пониженным уровнем"
    )
    high_level: RiskFactorInfo = Field(
        ..., 
        description="Информация о показателях с повышенным уровнем"
    )
    chronical: RiskFactorInfo = Field(
        ..., 
        description="Информация о хронических заболеваниях"
    )

    class Config:
        schema_extra = {
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