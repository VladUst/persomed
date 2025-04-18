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
    summary="Предсказать заболевания по симптомам",
    description="""
    Эндпоинт принимает список симптомов и возвращает предсказания заболеваний, используя как модель
    машинного обучения, так и онтологический подход.
    
    Модель машинного обучения использует MultinomialNB (Наивный Байесовский классификатор) для определения
    наиболее вероятных заболеваний на основе представленных симптомов.
    
    Онтологический подход использует семантические связи между симптомами и заболеваниями
    для определения всех возможных заболеваний, соответствующих предоставленным симптомам.
    """
)
async def predict_disease(
    data: SymptomsList = Body(
        ...,
        example={"symptoms": ["головная боль", "тошнота", "высокая температура"]},
        description="Список симптомов для диагностики"
    )
):
    """
    Предсказание заболеваний на основе списка симптомов.
    
    Использует два метода:
    1. Модель машинного обучения для предсказания до 3 наиболее вероятных заболеваний
    2. Онтологию для определения списка возможных заболеваний
    
    - **symptoms**: Список симптомов для анализа
    
    Возвращает:
    - **ml_prediction**: Список наиболее вероятных заболеваний (до 3) по результатам машинного обучения
    - **ontology_prediction**: Список заболеваний, соответствующих симптомам по онтологии
    - **model_info**: Информация о модели машинного обучения и её метриках
    - **ontology_info**: Информация об онтологии заболеваний
    
    Пример запроса:
    ```json
    {
        "symptoms": ["головная боль", "тошнота", "высокая температура"]
    }
    ```
    
    Пример ответа:
    ```json
    {
        "ml_prediction": ["Грипп", "Мигрень", "ОРВИ"],
        "ontology_prediction": ["Грипп", "Мигрень", "Менингит"],
        "model_info": "Модель диагностики заболеваний по перечню симптомов. Модель имеет точность: 0.9534, f-меру: 0.9428",
        "ontology_info": "Онтология заболеваний. Онтология связывает 90 симптомов и 135 заболеваний"
    }
    ```
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