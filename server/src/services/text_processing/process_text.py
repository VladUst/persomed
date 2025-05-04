from typing import List, Dict, Optional, Any
import os
import json
from medcat.cat import CAT
from src.services.translate.translate import translate_to_english, translate_to_russian


class TextProcessingService:
    """
    Singleton service for medical text processing using MedCAT.
    """
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TextProcessingService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.cat = self._initialize_medcat()
            self._initialized = True
    
    @staticmethod
    def get_instance():
        """
        Get singleton instance of TextProcessingService.
        
        Returns:
            TextProcessingService: Singleton instance
        """
        if TextProcessingService._instance is None:
            return TextProcessingService()
        return TextProcessingService._instance
    
    def _initialize_medcat(self) -> CAT:
        """
        Initialize and load the MedCAT model with UMLS.
        
        Returns:
            CAT: Initialized MedCAT model
        """
        print("Initializing MedCAT with UMLS model...")
        
        # Путь к директории с моделью
        model_dir = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(model_dir, "models", "umls_small_model")
        model_zip_path = os.path.join(model_dir, "models", "umls_small_model.zip")
        
        # Пытаемся загрузить модель из распакованной директории
        if os.path.exists(model_path) and os.path.isdir(model_path):
            print(f"Загружаем модель UMLS из распакованной директории: {model_path}")
            
            try:
                # Загружаем модель напрямую из директории
                cat = CAT.load_model_pack(model_path)
                print("Модель успешно загружена из директории!")
            except Exception as e:
                print(f"Ошибка при загрузке из директории: {e}")
                print("Попытка загрузки из ZIP-архива...")
                if os.path.exists(model_zip_path):
                    cat = CAT.load_model_pack(model_zip_path)
                    print("Модель успешно загружена из ZIP-архива!")
                else:
                    raise FileNotFoundError(f"Модель не найдена в архиве: {model_zip_path}")
        else:
            # Если директория не существует, пытаемся загрузить из архива
            if os.path.exists(model_zip_path):
                print(f"Загружаем модель UMLS из архива: {model_zip_path}")
                cat = CAT.load_model_pack(model_zip_path)
                print("Модель успешно загружена из ZIP-архива!")
            else:
                raise FileNotFoundError(f"Модель не найдена ни в директории {model_path}, ни в архиве {model_zip_path}")
        
        # Отключаем режим обучения
        cat.train = False
        
        print("Модель UMLS успешно загружена!")
        return cat
    
    async def process_medical_text(self, text: str, language: str = "ru") -> List[Dict[str, Any]]:
        """
        Process medical text using MedCAT and extract named entities with their attributes.
        Support both English and Russian texts.
        
        Args:
            text (str): Medical text to process
            language (str): Input text language ("en" or "ru")
            
        Returns:
            List[Dict[str, Any]]: List of named entities with their attributes (CUI, TUI, name, definition, ICD code)
        """
        try:
            processed_text = text
            
            # Если текст на русском, переводим его на английский
            if language == "ru":
                processed_text = await translate_to_english(text)
            
            # Обрабатываем текст с помощью MedCAT
            entities = self.cat.get_entities(processed_text)
            
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
                    
                    # Если язык русский, переводим name и types на русский
                    if language == "ru":
                        name = await translate_to_russian(name)
                        if types:
                            types = await translate_to_russian(types)
                    
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


# Глобальная функция-обёртка для совместимости с существующим кодом
async def process_medical_text(text: str, language: str = "ru") -> List[Dict[str, Any]]:
    """
    Global wrapper function for processing medical text (for backward compatibility).
    
    Args:
        text (str): Medical text to process
        language (str): Input text language ("en" or "ru")
        
    Returns:
        List[Dict[str, Any]]: List of named entities with their attributes
    """
    service = TextProcessingService.get_instance()
    return await service.process_medical_text(text, language)