from datetime import datetime
import re
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.medical_documents import (
    DiseasesHistoryDocRepository,
    RecommendationsDocRepository
)
from src.services.risk_analysis.get_risk_factors import get_risk_factors
from src.services.text_processing.process_text import process_medical_text
from src.services.diagnostic import get_predictions


async def get_symptoms(session: AsyncSession) -> List[Dict[str, str]]:
    """
    Извлекает симптомы из анамнезов.
    
    Args:
        session: Асинхронная сессия базы данных
        
    Returns:
        List[Dict[str, str]]: Список симптомов
    """
    # Получаем все документы из истории болезней
    repository = DiseasesHistoryDocRepository(session)
    documents = await repository.get_all_with_details()
    
    # Фильтруем только анамнезы с деталями
    anamnesis_docs = [
        doc for doc in documents 
        if doc.type == "Анамнез" and doc.details is not None
    ]
    
    symptoms = []
    
    # Для каждого анамнеза
    for doc in anamnesis_docs:
        # Проверяем наличие anamnesis непосредственно в details
        if not hasattr(doc.details, "anamnesis"):
            continue
        
        anamnesis_text = doc.details.anamnesis
        
        if not anamnesis_text:
            continue
        
        # Обрабатываем текст через сервис обработки текстов
        concepts = await process_medical_text(anamnesis_text)
        
        # Извлекаем только симптомы (type_ids содержит T184)
        for concept in concepts:
            if "T184" in concept.get("type_ids", []):
                symptoms.append({
                    "name": concept.get("name", ""),
                    "source": f"Автоматически извлечен из анамнеза: {doc.name}",
                    "date": doc.date
                })
    
    return symptoms


async def get_diseases(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Извлекает 5 последних заболеваний из истории болезней, исключая тип "Анамнез".
    
    Args:
        session: Асинхронная сессия базы данных
        
    Returns:
        List[Dict[str, Any]]: Список заболеваний
    """
    repository = DiseasesHistoryDocRepository(session)
    diseases = await repository.get_all()
    
    # Фильтруем, исключая документы типа "Анамнез"
    diseases = [d for d in diseases if d.type != "Анамнез"]
    
    # Сортируем по дате (новые в начале) и берем 5 последних
    diseases.sort(key=lambda x: x.date, reverse=True)
    diseases = diseases[:5]
    
    # Форматируем результат
    result = []
    for disease in diseases:
        result.append({
            "id": disease.id,
            "name": disease.name,
            "type": disease.type,
            "date": disease.date,
            "icd_code": disease.icd_code
        })
    
    return result


async def get_rates(session: AsyncSession) -> List[Dict[str, str]]:
    """
    Возвращает оценки рисков заболеваний по категориям.
    
    Args:
        session: Асинхронная сессия базы данных
        
    Returns:
        List[Dict[str, str]]: Список оценок рисков
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    return [
        {
            "name": "Сердечно-сосудистые заболевания",
            "rate": "Высокие",
            "source": "Ручная оценка",
            "date": current_date
        },
        {
            "name": "Заболевания эндокринной системы",
            "rate": "Высокие",
            "source": "Ручная оценка",
            "date": current_date
        },
        {
            "name": "Заболевания системы пищеварения",
            "rate": "Средние",
            "source": "Ручная оценка",
            "date": current_date
        },
        {
            "name": "Заболевания органов дыхания",
            "rate": "Низкие",
            "source": "Ручная оценка",
            "date": current_date
        },
        {
            "name": "Заболевания почек и мочевыделительной системы",
            "rate": "Низкие",
            "source": "Ручная оценка",
            "date": current_date
        },
        {
            "name": "Заболевания опорно-двигательного аппарата",
            "rate": "Низкие",
            "source": "Ручная оценка",
            "date": current_date
        },
        {
            "name": "Заболевания кожи и волосяных покровов",
            "rate": "Неизвестно",
            "source": "Ручная оценка",
            "date": current_date
        }
    ]


async def get_suspicions(symptoms: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Возвращает подозрения на заболевания на основе симптомов.
    
    Args:
        symptoms: Список симптомов из предыдущего шага
        
    Returns:
        List[Dict[str, str]]: Список подозрений на заболевания
    """    
    # Если симптомов нет, возвращаем пустой список
    if not symptoms:
        return []
    
    # Группируем симптомы по источнику (документу анамнеза)
    symptoms_by_source = {}
    for symptom in symptoms:
        source = symptom["source"]
        if source not in symptoms_by_source:
            symptoms_by_source[source] = []
        symptoms_by_source[source].append(symptom["name"])
    
    suspicions = []
    
    # Для каждого источника делаем отдельное предсказание
    for source, symptom_list in symptoms_by_source.items():
        try:
            # Получаем предсказания от сервиса диагностики
            prediction_data = await get_predictions(symptom_list)
            
            # Получаем предсказания из модели машинного обучения
            ml_predictions = prediction_data["ml"]["prediction"]
            
            # Выбираем первое предсказание (наиболее вероятное)
            # Если в предсказаниях есть "Диабет", выбираем его
            selected_disease = None
            for disease in ml_predictions:
                if "диабет" in disease.lower():
                    selected_disease = disease
                    break
            
            # Если диабет не найден, берем первое предсказание
            if not selected_disease and ml_predictions:
                selected_disease = ml_predictions[0]
            
            if selected_disease:
                suspicion = {
                    "name": selected_disease,
                    "date": prediction_data["ml"]["date"],
                    "source": prediction_data["ml"]["info"],
                    "icd": ""
                }
                suspicions.append(suspicion)
        
        except Exception as e:
            print(f"Ошибка при получении предсказания: {e}")
    
    return suspicions


async def get_risks(session: AsyncSession) -> Dict[str, Dict[str, str]]:
    """
    Возвращает факторы риска.
    
    Args:
        session: Асинхронная сессия базы данных
        
    Returns:
        Dict[str, Dict[str, str]]: Факторы риска
    """
    return await get_risk_factors(session)


async def get_drugs(session: AsyncSession) -> List[Dict[str, str]]:
    """
    Возвращает назначенные препараты.
    
    Args:
        session: Асинхронная сессия базы данных
        
    Returns:
        List[Dict[str, str]]: Список назначенных препаратов
    """
    repository = RecommendationsDocRepository(session)
    recommendations = await repository.get_all_with_details()
    
    # Фильтруем рекомендации типа "Назначения" и с деталями
    prescriptions = [
        r for r in recommendations 
        if r.type == "Назначения" and r.details is not None
    ]
    
    drugs = []
    for prescription in prescriptions:
        
        # Проверяем, что есть instructions напрямую в деталях
        if not hasattr(prescription.details, "instructions"):
            continue
        
        instructions = prescription.details.instructions
        # Разбиваем строку препаратов по запятой
        drugs_list = instructions.split(",")
        
        for drug_info in drugs_list:
            drug_info = drug_info.strip()
            
            # Извлекаем название препарата и дозировку
            # Паттерн для разделения названия и дозировки
            match = re.match(r"(.*?)\s+(\d+\s*(?:мг|мл|г|таб)\.?(?:/(?:ден|сут))?\.?)", drug_info)
            
            if match:
                name, dosage = match.groups()
                name = name.strip()
                # Делаем первую букву названия препарата заглавной
                capitalized_name = name[0].upper() + name[1:] if name else ""
                
                drugs.append({
                    "name": capitalized_name,
                    "dosage": dosage.strip(),
                    "date": prescription.details.date if hasattr(prescription.details, "date") else prescription.date
                })
            else:
                # Если не удалось разделить, просто берем всю строку как название
                # Делаем первую букву заглавной
                capitalized_name = drug_info[0].upper() + drug_info[1:] if drug_info else ""
                
                drugs.append({
                    "name": capitalized_name,
                    "dosage": "Не указано",
                    "date": prescription.details.date if hasattr(prescription.details, "date") else prescription.date
                })
    
    return drugs


async def get_recommendations(session: AsyncSession) -> List[Dict[str, str]]:
    """
    Возвращает рекомендации.
    
    Args:
        session: Асинхронная сессия базы данных
        
    Returns:
        List[Dict[str, str]]: Список рекомендаций
    """
    repository = RecommendationsDocRepository(session)
    recommendations_docs = await repository.get_all_with_details()
    
    # Фильтруем рекомендации типа "Рекомендации" и с деталями
    filtered_recommendations = [
        r for r in recommendations_docs 
        if r.type == "Рекомендации" and r.details is not None
    ]
    
    recommendations = []
    for rec_doc in filtered_recommendations:
        
        # Проверяем, что есть instructions напрямую в деталях
        if not hasattr(rec_doc.details, "instructions"):
            continue
        
        instructions = rec_doc.details.instructions
        rec_list = instructions.split(",")
        
        for rec_text in rec_list:
            rec_text = rec_text.strip()
            if rec_text:  # Проверка, что рекомендация не пустая
                # Делаем первую букву заглавной
                capitalized_rec = rec_text[0].upper() + rec_text[1:] if rec_text else ""
                
                recommendations.append({
                    "name": capitalized_rec,
                    "source": rec_doc.name,
                    "date": rec_doc.details.date if hasattr(rec_doc.details, "date") else rec_doc.date
                })
    
    return recommendations


async def get_patient_status(session: AsyncSession) -> Dict[str, Any]:
    """
    Возвращает полный статус пациента.
    
    Args:
        session: Асинхронная сессия базы данных
        
    Returns:
        Dict[str, Any]: Полный статус пациента
    """
    symptoms = await get_symptoms(session)
    diseases = await get_diseases(session)
    rates = await get_rates(session)
    suspicions = await get_suspicions(symptoms)  # Передаем симптомы напрямую
    risks = await get_risks(session)
    drugs = await get_drugs(session)
    recommendations = await get_recommendations(session)
    
    return {
        "symptoms": symptoms,
        "diseases": diseases,
        "rates": rates,
        "suspicions": suspicions,
        "risks": risks,
        "drugs": drugs,
        "recommendations": recommendations
    } 