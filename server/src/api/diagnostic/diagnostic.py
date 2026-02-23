from fastapi import APIRouter, status, Body
from datetime import datetime

from src.schemas.diagnostic import SymptomsList, PredictionResponse
from src.services.diagnostic.ml_disease_prediction.get_prediction import get_prediction as ml_get_prediction
from src.services.diagnostic.ontology_diseases_prediction.get_prediction import get_prediction as ontology_get_prediction
from src.services.diagnostic.ml_disease_prediction.get_prediction import get_model_info
from src.services.diagnostic.ontology_diseases_prediction.get_prediction import get_ontology_info
from src.services.translate import translate_to_english, translate_to_russian

diagnostic_router = APIRouter(
    tags=["Сервис диагностики"]
)


@diagnostic_router.post(
    "/diseases", 
    response_model=PredictionResponse, 
    status_code=status.HTTP_200_OK, 
    summary="Предсказать заболевания по симптомам",
    responses={
        200: {
            "description": "Успешный ответ с предсказаниями заболеваний",
            "content": {
                "application/json": {
                    "example": {
                        "ml": {
                            "prediction": ["Грипп", "Пневмония", "ОРВИ"],
                            "info": "Модель диагностики заболеваний по перечню симптомов. Модель имеет точность: 0.9534, f-меру: 0.9428",
                            "date": "26.07.2023"
                        },
                        "ontology": {
                            "prediction": ["Грипп", "Острый ринит", "Синусит"],
                            "info": "Онтология заболеваний. Онтология связывает 90 симптомов и 135 заболеваний",
                            "date": "26.07.2023"
                        }
                    }
                }
            }
        }
    }
)
async def diseases(
    data: SymptomsList = Body(
        ...,
        example={"symptoms": ["кашель", "охриплость", "стридор"]},
    )
):
    """
    Диагностика возможных заболеваний на основе списка симптомов пациента.
    
    Метод использует два параллельных подхода для диагностики:
    1. Модель машинного обучения (MultinomialNB) для определения до 3 наиболее вероятных заболеваний
    2. Медицинскую онтологию для выявления всех заболеваний, связанных с указанными симптомами
    
    Входные параметры:
    - **symptoms**: Список симптомов пациента в текстовом формате (на русском языке)
    
    Выходные параметры:
    - **ml**: Результаты предсказания с использованием машинного обучения
      - prediction: До трех наиболее вероятных заболеваний (на русском языке)
      - info: Информация о модели и её метриках
      - date: Дата предсказания
    - **ontology**: Результаты предсказания с использованием онтологии
      - prediction: Список заболеваний, соответствующих симптомам (на русском языке)
      - info: Информация об онтологии
      - date: Дата предсказания
    """
    # Получаем текущую дату
    current_date = datetime.now().strftime("%d.%m.%Y")
    
    # Переводим симптомы с русского на английский
    english_symptoms = await translate_to_english(data.symptoms)
    
    # Получаем предсказания от модели машинного обучения (на английском)
    ml_results_en = ml_get_prediction(english_symptoms)
    
    # Получаем предсказания на основе онтологии (на английском)
    ontology_results_en = ontology_get_prediction(english_symptoms)
    
    # Переводим результаты обратно на русский
    ml_results_ru = await translate_to_russian(ml_results_en)
    ontology_results_ru = await translate_to_russian(ontology_results_en)
    
    # Получаем информацию о модели и онтологии
    model_info = get_model_info()
    ontology_info = get_ontology_info()
    
    return {
        "ml": {
            "prediction": ml_results_ru,
            "info": model_info,
            "date": current_date
        },
        "ontology": {
            "prediction": ontology_results_ru,
            "info": ontology_info,
            "date": current_date
        }
    } 