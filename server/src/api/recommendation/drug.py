from fastapi import APIRouter, status, Body

from src.schemas.recommendation import DiseaseRequest, DrugRecommendationResponse
from src.services.recommendation.drug_recommendation import get_drug_recommendations, get_ontology_info, get_current_date
from src.services.translate import translate_to_english, translate_to_russian

# Создаем роутер для рекомендаций препаратов
router = APIRouter(
    tags=["Сервис рекомендаций"]
)


@router.post(
    "/drugs", 
    response_model=DrugRecommendationResponse, 
    status_code=status.HTTP_200_OK, 
    summary="Получить рекомендации препаратов по заболеванию"
)
async def recommend_drugs(
    data: DiseaseRequest = Body(
        ...,
        example={"disease": "Пневмония"},
    )
):
    """
    Получение рекомендаций по лекарственным препаратам для лечения заданного заболевания.
    
    Метод использует онтологию заболеваний и препаратов для определения подходящих лекарств
    на основе семантических связей между заболеваниями и препаратами, которые их лечат.
    
    Входные параметры:
    - **disease**: Название заболевания, для которого требуются рекомендации препаратов (на русском языке)
    
    Выходные параметры:
    - **recommendations**: Список рекомендованных лекарственных препаратов для лечения заболевания (на русском языке)
    - **info**: Информация об онтологии заболеваний и препаратов (количество заболеваний и препаратов)
    - **date**: Дата формирования рекомендации в формате ДД.ММ.ГГГГ
    """
    # Переводим название заболевания с русского на английский
    disease_en = await translate_to_english(data.disease)
    
    # Получаем рекомендации препаратов для заболевания на английском
    drug_recommendations_en = get_drug_recommendations(disease_en)
    
    # Переводим рекомендации обратно на русский
    drug_recommendations_ru = await translate_to_russian(drug_recommendations_en)
    
    # Получаем информацию об онтологии
    ontology_info = get_ontology_info()
    
    # Получаем текущую дату
    current_date = get_current_date()
    
    return {
        "recommendations": drug_recommendations_ru,
        "info": ontology_info,
        "date": current_date
    } 