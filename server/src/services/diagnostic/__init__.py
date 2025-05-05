from src.services.diagnostic.ml_disease_prediction.get_prediction import get_prediction as ml_disease_prediction
from src.services.diagnostic.ontology_diseases_prediction.get_prediction import get_prediction as ontology_diseases_prediction
from src.services.diagnostic.ml_disease_prediction.get_prediction import get_model_info
from src.services.diagnostic.ontology_diseases_prediction.get_prediction import get_ontology_info
from src.services.translate import translate_to_english, translate_to_russian
from datetime import datetime
from typing import List, Dict, Any


async def analyze_symptoms(symptoms):
    """
    Анализирует симптомы и возвращает результаты.
    Обертка для удобства вызова.
    
    Args:
        symptoms: Список симптомов для анализа
        
    Returns:
        Результаты анализа симптомов
    """
    return await ml_disease_prediction(symptoms)


async def predict_disease(symptoms):
    """
    Предсказывает заболевание на основе симптомов.
    Обертка для удобства вызова.
    
    Args:
        symptoms: Список симптомов для предсказания
        
    Returns:
        Предсказанное заболевание
    """
    return await ontology_diseases_prediction(symptoms)


async def get_predictions(symptoms_list: List[str]) -> Dict[str, Any]:
    """
    Получает предсказания заболеваний по списку симптомов, используя ML модель и онтологию.
    
    Args:
        symptoms_list: Список симптомов на русском языке
        
    Returns:
        Dict[str, Any]: Результаты предсказания в формате
        {
            "ml": {"prediction": [...], "info": "...", "date": "..."},
            "ontology": {"prediction": [...], "info": "...", "date": "..."}
        }
    """
    # Получаем текущую дату
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Переводим симптомы с русского на английский
    english_symptoms = await translate_to_english(symptoms_list)
    
    # Получаем предсказания от модели машинного обучения (на английском)
    ml_results_en = ml_disease_prediction(english_symptoms)
    
    # Получаем предсказания на основе онтологии (на английском)
    ontology_results_en = ontology_diseases_prediction(english_symptoms)
    
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


__all__ = [
    "ml_disease_prediction", 
    "ontology_diseases_prediction",
    "get_model_info",
    "get_ontology_info",
    "analyze_symptoms",
    "predict_disease",
    "get_predictions"
] 