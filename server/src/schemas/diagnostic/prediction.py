from typing import List
from pydantic import BaseModel, Field


class SymptomsList(BaseModel):
    symptoms: List[str] = Field(description="Список симптомов для диагностики")


class PredictionResponse(BaseModel):
    ml_prediction: List[str] = Field(description="Наиболее вероятные заболевания по результатам машинного обучения (до 3)")
    ontology_prediction: List[str] = Field(description="Список заболеваний, соответствующих симптомам по онтологии")
    model_info: str = Field(description="Информация о модели машинного обучения и её метриках")
    ontology_info: str = Field(description="Информация об онтологии заболеваний") 