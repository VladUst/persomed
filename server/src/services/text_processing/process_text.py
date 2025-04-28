from typing import List, Dict, Optional, Any
import os
import json
from medcat.cat import CAT


def initialize_medcat() -> CAT:
    """
    Initialize and load the MedCAT model with UMLS.
    
    Returns:
        CAT: Initialized MedCAT model
    """
    print("Initializing MedCAT with UMLS model...")
    
    # Путь к модели в архиве
    model_dir = os.path.dirname(os.path.realpath(__file__))
    model_path = os.path.join(model_dir, "models", "umls_small_model.zip")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Модель не найдена по пути: {model_path}")
    
    print(f"Загружаем модель UMLS из архива: {model_path}")
    
    # Загружаем модель из архива
    cat = CAT.load_model_pack(model_path)
    
    # Отключаем режим обучения
    cat.train = False
    
    print("Модель UMLS успешно загружена!")
    return cat


# Singleton instance of MedCAT model
_medcat_instance = None


def get_medcat_instance() -> CAT:
    """
    Get the MedCAT instance (singleton pattern).
    
    Returns:
        CAT: MedCAT instance
    """
    global _medcat_instance
    if _medcat_instance is None:
        _medcat_instance = initialize_medcat()
    return _medcat_instance


def process_medical_text(text: str) -> List[Dict[str, Any]]:
    """
    Process medical text using MedCAT and extract named entities with their attributes.
    
    Args:
        text (str): Medical text to process
        
    Returns:
        List[Dict[str, Any]]: List of named entities with their attributes (CUI, TUI, name, definition, ICD code)
    """
    try:
        cat = get_medcat_instance()
        
        # Обрабатываем текст с помощью MedCAT
        entities = cat.get_entities(text)
        
        # Создаем результат
        result = []
        
        # Обрабатываем сущности
        for entity_id, entity_data in entities.get('entities').items():
            try:
                # Проверяем уверенность
                confidence = entity_data.get('acc', 0)
                
                # Получаем основные данные
                cui = entity_data.get('cui', '')
                pretty_name = entity_data.get('pretty_name', '')
                detected_name = entity_data.get('detected_name', '')
                name = pretty_name if pretty_name else detected_name
                
                # Получаем типы (TUI) и types
                type_ids = entity_data.get('type_ids', [])
                types = entity_data.get('types', [])
                
                # Получаем определение (если доступно)
                definition = ""
                
                # Получаем все коды МКБ-10 как есть
                icd10 = entity_data.get('icd10', [])
                
                # Получаем позиции
                start_index = entity_data.get('start', 0)
                end_index = entity_data.get('end', 0)
                source_text = entity_data.get('source_value', '')
                
                # Создаем объект сущности
                entity_obj = {
                    "cui": cui,
                    "type_ids": type_ids,
                    "types": types,
                    "name": name, 
                    "definition": definition,
                    "icd10": icd10,
                    "start_index": start_index,
                    "end_index": end_index,
                    "source_text": source_text,
                    "confidence": confidence
                }
                
                result.append(entity_obj)
                
            except Exception as e:
                print(f"Ошибка при обработке сущности {entity_id}: {e}")
                continue
    
        return result
        
    except Exception as e:
        print(f"Общая ошибка при обработке текста: {e}")
        return []