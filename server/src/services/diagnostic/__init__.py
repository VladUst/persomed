from src.services.diagnostic.ml_disease_prediction.get_prediction import get_prediction as ml_disease_prediction
from src.services.diagnostic.ontology_diseases_prediction.get_prediction import get_prediction as ontology_diseases_prediction
from src.services.diagnostic.ml_disease_prediction.get_prediction import get_model_info
from src.services.diagnostic.ontology_diseases_prediction.get_prediction import get_ontology_info


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


__all__ = [
    "ml_disease_prediction", 
    "ontology_diseases_prediction",
    "get_model_info",
    "get_ontology_info",
    "analyze_symptoms",
    "predict_disease"
] 