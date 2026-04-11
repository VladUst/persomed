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


async def get_symptoms(session: AsyncSession, patient_id: int) -> List[Dict[str, str]]:
    """
    Извлекает симптомы из анамнезов.
    
    Args:
        session: Асинхронная сессия базы данных
        patient_id: Идентификатор пациента
        
    Returns:
        List[Dict[str, str]]: Список симптомов
    """
    repository = DiseasesHistoryDocRepository(session)
    documents = await repository.get_all_with_details_by_patient(patient_id)
    
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


async def get_diseases(session: AsyncSession, patient_id: int) -> List[Dict[str, Any]]:
    """
    Извлекает 5 последних заболеваний из истории болезней, исключая тип "Анамнез".
    
    Args:
        session: Асинхронная сессия базы данных
        patient_id: Идентификатор пациента
        
    Returns:
        List[Dict[str, Any]]: Список заболеваний
    """
    repository = DiseasesHistoryDocRepository(session)
    diseases = await repository.get_all_by_patient(patient_id)
    
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


async def get_rates(session: AsyncSession, patient_id: int) -> List[Dict[str, str]]:
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
    
    for source, symptom_list in symptoms_by_source.items():
        try:
            # Получаем предсказания от сервиса диагностики
            prediction_data = await get_predictions(symptom_list)
            
            ml_predictions = prediction_data["ml"]["prediction"]
            
            selected_disease = None
            
            if not selected_disease and ml_predictions:
                selected_disease = ml_predictions[1]
            
            if selected_disease:
                suspicion = {
                    "name": selected_disease,
                    "date": prediction_data["ml"]["date"],
                    "source": prediction_data["ml"]["info"],
                }
                suspicions.append(suspicion)
        
        except Exception as e:
            print(f"Ошибка при получении предсказания: {e}")
    
    return suspicions


async def get_risks(session: AsyncSession, patient_id: int) -> Dict[str, Dict[str, str]]:
    """
    Возвращает факторы риска.
    
    Args:
        session: Асинхронная сессия базы данных
        patient_id: Идентификатор пациента
        
    Returns:
        Dict[str, Dict[str, str]]: Факторы риска
    """
    return await get_risk_factors(session, patient_id)


async def get_drugs(session: AsyncSession, patient_id: int) -> List[Dict[str, str]]:
    """
    Возвращает назначенные препараты.
    
    Args:
        session: Асинхронная сессия базы данных
        patient_id: Идентификатор пациента
        
    Returns:
        List[Dict[str, str]]: Список назначенных препаратов
    """
    repository = RecommendationsDocRepository(session)
    recommendations = await repository.get_all_with_details_by_patient(patient_id)
    
    # Фильтруем рекомендации типа "Назначения" и с деталями
    prescriptions = [
        r for r in recommendations 
        if r.type == "Назначения" and r.details is not None
    ]
    
    drugs = []
    for prescription in prescriptions:
        if not hasattr(prescription.details, "instructions"):
            continue

        instructions = prescription.details.instructions
        if not instructions:
            continue

        doc_date = prescription.details.date if hasattr(prescription.details, "date") else prescription.date
        concepts = await process_medical_text(instructions)

        for concept in concepts:
            type_ids = concept.get("type_ids", [])
            if "T200" not in type_ids and "T121" not in type_ids:
                continue

            full_name = concept.get("name", "")
            if not full_name:
                continue

            if "T200" in type_ids:
                # T200 — клинический препарат, дозировка уже в имени: "Эналаприл 10 мг"
                dose_match = re.search(r"(\d+(?:[.,]\d+)?\s*(?:мг|мл|г|ME|ед)(?:/(?:кг|сут|ден|мл))?)", full_name, re.IGNORECASE)
                if dose_match:
                    dosage = dose_match.group(1).strip()
                    name = full_name[: dose_match.start()].strip()
                else:
                    dosage = "-"
                    name = full_name.strip()
            else:
                # T121 — фармакологическое вещество, дозировки в имени нет
                dosage = "-"
                name = full_name.strip()

            capitalized_name = name[0].upper() + name[1:] if name else ""
            drugs.append({"name": capitalized_name, "dosage": dosage, "date": doc_date, "source": prescription.name})

    return drugs


async def get_recommendations(session: AsyncSession, patient_id: int) -> List[Dict[str, str]]:
    """
    Возвращает рекомендации.
    
    Args:
        session: Асинхронная сессия базы данных
        patient_id: Идентификатор пациента
        
    Returns:
        List[Dict[str, str]]: Список рекомендаций
    """
    repository = RecommendationsDocRepository(session)
    recommendations_docs = await repository.get_all_with_details_by_patient(patient_id)
    
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


async def get_patient_status(session: AsyncSession, patient_id: int) -> Dict[str, Any]:
    """
    Возвращает полный статус пациента.
    
    Args:
        session: Асинхронная сессия базы данных
        patient_id: Идентификатор пациента
        
    Returns:
        Dict[str, Any]: Полный статус пациента
    """
    symptoms = await get_symptoms(session, patient_id)
    diseases = await get_diseases(session, patient_id)
    rates = await get_rates(session, patient_id)
    suspicions = await get_suspicions(symptoms)
    risks = await get_risks(session, patient_id)
    drugs = await get_drugs(session, patient_id)
    recommendations = await get_recommendations(session, patient_id)
    
    return {
        "symptoms": symptoms,
        "diseases": diseases,
        "rates": rates,
        "suspicions": suspicions,
        "risks": risks,
        "drugs": drugs,
        "recommendations": recommendations
    } 