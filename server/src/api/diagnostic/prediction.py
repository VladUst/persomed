from fastapi import APIRouter, status, Body
from typing import List

from src.schemas.diagnostic import SymptomsList, PredictionResponse
from src.services.diagnostic.ml_disease_prediction.get_prediction import get_prediction as ml_get_prediction
from src.services.diagnostic.ontology_diseases_prediction.get_prediction import get_prediction as ontology_get_prediction
from src.services.diagnostic.ml_disease_prediction.get_prediction import get_model_info
from src.services.diagnostic.ontology_diseases_prediction.get_prediction import get_ontology_info

# Создаем роутер для предсказания заболеваний
router = APIRouter(
    tags=["Сервис диагностики"]
)


@router.post(
    "/predict", 
    response_model=PredictionResponse, 
    status_code=status.HTTP_200_OK, 
    summary="Предсказать заболевания по симптомам"
)
async def predict_disease(
    data: SymptomsList = Body(
        ...,
        example={"symptoms": ["головная боль", "тошнота", "высокая температура"]},
    )
):
    """
    Диагностика возможных заболеваний на основе списка симптомов пациента.
    
    Метод использует два параллельных подхода для диагностики:
    1. Модель машинного обучения (MultinomialNB) для определения до 3 наиболее вероятных заболеваний
    2. Медицинскую онтологию для выявления всех заболеваний, связанных с указанными симптомами
    
    Входные параметры:
    - **symptoms**: Список симптомов пациента в текстовом формате
    
    Выходные параметры:
    - **ml_prediction**: До трех наиболее вероятных заболеваний по оценке модели машинного обучения
    - **ontology_prediction**: Список всех заболеваний, связанных с указанными симптомами согласно онтологии
    - **model_info**: Информация о модели машинного обучения, включая метрики точности и F-меру
    - **ontology_info**: Информация об используемой онтологии заболеваний
    """
    # Получаем предсказания от модели машинного обучения
    ml_results = ml_get_prediction(data.symptoms)
    
    # Получаем предсказания на основе онтологии
    ontology_results = ontology_get_prediction(data.symptoms)
    
    # Получаем информацию о модели и онтологии
    model_info = get_model_info()
    ontology_info = get_ontology_info()
    
    return {
        "ml_prediction": ml_results,
        "ontology_prediction": ontology_results,
        "model_info": model_info,
        "ontology_info": ontology_info
    } 