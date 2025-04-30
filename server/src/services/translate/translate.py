from deep_translator import GoogleTranslator
from abc import ABC, abstractmethod
from typing import List, Union, Dict, Optional

# Create a custom base class to replace BaseTranslator
class CustomBaseTranslator(ABC):
    """
    Custom abstract base class for translator implementations
    """
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target
    
    @abstractmethod
    def translate(self, text: str) -> str:
        """
        Abstract method that should be implemented by translator classes
        """
        pass

# Медицинский словарь для частых терминов, которые плохо переводятся
MED_DICT_EN_RU = {
    "sign or symptom": "Признак или Симптом",
    "cough": "кашель",
    "fever": "лихорадка",
    "shortness of breath": "одышка",
    "dyspnea": "одышка",
    "fatigue": "утомляемость",
    "chest pain": "боль в груди",
    "sore throat": "боль в горле",
    "hoarseness": "охриплость",
    "headache": "головная боль",
    "deglutition disorder": "расстройство глотания",
    "pneumonia": "пневмония",
    "bronchitis": "бронхит",
    "asthma": "астма",
    "influenza": "грипп",
    "flu": "грипп",
    "common cold": "простуда",
    "congestive heart failure": "сердечная недостаточность",
    "failure heart congestive": "сердечная недостаточность",
    "heart failure": "сердечная недостаточность",
    "hypertension": "гипертония",
    "legionnaires' disease": "легионеллёз",
    "mycoplasma pneumoniae infection": "микоплазменная пневмония",
    "tuberculosis": "туберкулёз",
    "copd": "хобл",
    "chronic obstructive pulmonary disease": "хроническая обструктивная болезнь лёгких",
    "sinusitis": "синусит",
    "rhinitis": "ринит",
    "tonsilitis": "тонзиллит",
    "pharyngitis": "фарингит",
    "laryngitis": "ларингит"
}

# Обратный словарь
MED_DICT_RU_EN = {v.lower(): k for k, v in MED_DICT_EN_RU.items()}

class MedicalTranslator(CustomBaseTranslator):
    """
    Кастомный переводчик для медицинских терминов, использующий словарь и GoogleTranslator
    """
    def __init__(self, source: str, target: str, dict_ru_en: Dict[str, str], dict_en_ru: Dict[str, str]):
        """
        Инициализация переводчика с медицинским словарем
        
        Args:
            source: Исходный язык (ru, en)
            target: Целевой язык (ru, en)
            dict_ru_en: Словарь русско-английских терминов
            dict_en_ru: Словарь англо-русских терминов
        """
        super().__init__(source=source, target=target)
        self._dict_ru_en = dict_ru_en
        self._dict_en_ru = dict_en_ru
        self._google_translator = GoogleTranslator(source=source, target=target)
    
    def translate(self, text: str) -> str:
        """
        Перевод текста с использованием словаря и GoogleTranslator в качестве запасного варианта
        
        Args:
            text: Текст для перевода
            
        Returns:
            Переведенный текст
        """
        text_lower = text.lower()
        
        # Выбираем словарь в зависимости от направления перевода
        if self.source == 'ru' and self.target == 'en':
            if text_lower in self._dict_ru_en:
                return self._dict_ru_en[text_lower]
        elif self.source == 'en' and self.target == 'ru':
            if text_lower in self._dict_en_ru:
                return self._dict_en_ru[text_lower]
        
        # Если слово не найдено в словаре, используем Google переводчик
        try:
            return self._google_translator.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Возвращаем исходный текст в случае ошибки

async def translate_to_english(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Translate Russian text or list of texts to English.
    Uses custom MedicalTranslator with dictionary for common terms and GoogleTranslator as a fallback.
    Result will be converted to lowercase to ensure case insensitivity.
    
    Args:
        text: Single string or list of strings in Russian
        
    Returns:
        Translated text in English, all lowercase
    """
    translator = MedicalTranslator(source='ru', target='en', dict_ru_en=MED_DICT_RU_EN, dict_en_ru=MED_DICT_EN_RU)
    
    if isinstance(text, str):
        try:
            translated = translator.translate(text)
            return translated.lower()
        except:
            # В случае ошибки возвращаем исходный текст
            return text.lower()
    
    # For lists, translate each item and convert to lowercase
    translated_list = []
    for item in text:
        try:
            translated = translator.translate(item)
            translated_list.append(translated.lower())
        except:
            translated_list.append(item.lower())
    
    return translated_list

async def translate_to_russian(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Translate English text or list of texts to Russian.
    Uses custom MedicalTranslator with dictionary for common terms and GoogleTranslator as a fallback.
    Result will have the first letter of each word capitalized.
    
    Args:
        text: Single string or list of strings in English
        
    Returns:
        Translated text in Russian with capitalized first letter
    """
    translator = MedicalTranslator(source='en', target='ru', dict_ru_en=MED_DICT_RU_EN, dict_en_ru=MED_DICT_EN_RU)
    
    if isinstance(text, str):
        try:
            translated = translator.translate(text)
            return translated.capitalize()
        except:
            # В случае ошибки возвращаем исходный текст
            return text.capitalize()
    
    # For lists, translate each item and capitalize
    translated_list = []
    for item in text:
        try:
            translated = translator.translate(item)
            translated_list.append(translated.capitalize())
        except:
            translated_list.append(item.capitalize())
    
    return translated_list