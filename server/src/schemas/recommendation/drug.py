from typing import List
from pydantic import BaseModel, Field


class DiseaseRequest(BaseModel):
    disease: str = Field(description="Название заболевания для поиска рекомендаций")


class DrugRecommendationResponse(BaseModel):
    recommendations: List[str] = Field(description="Список рекомендованных лекарственных препаратов")
    info: str = Field(description="Информация об онтологии заболеваний и препаратов")
    date: str = Field(description="Дата рекомендации в формате ДД.ММ.ГГГГ") 