from deep_translator import GoogleTranslator
from typing import List, Union

# Медицинский словарь для частых терминов, которые плохо переводятся
MED_DICT_EN_RU = {
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
    "congestive heart failure": "застойная сердечная недостаточность",
    "failure heart congestive": "застойная сердечная недостаточность",
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

async def translate_to_english(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Translate Russian text or list of texts to English.
    Uses medical dictionary for common terms and GoogleTranslator as a fallback.
    Result will be converted to lowercase to ensure case insensitivity.
    
    Args:
        text: Single string or list of strings in Russian
        
    Returns:
        Translated text in English, all lowercase
    """
    if isinstance(text, str):
        # Проверяем в словаре сначала
        text_lower = text.lower()
        if text_lower in MED_DICT_RU_EN:
            return MED_DICT_RU_EN[text_lower]
        
        # Если не нашли, используем GoogleTranslator
        translator = GoogleTranslator(source='ru', target='en')
        try:
            translated = translator.translate(text)
            return translated.lower()
        except:
            # В случае ошибки возвращаем исходный текст
            return text_lower
    
    # For lists, translate each item and convert to lowercase
    translated_list = []
    for item in text:
        # Проверяем в словаре сначала
        item_lower = item.lower()
        if item_lower in MED_DICT_RU_EN:
            translated_list.append(MED_DICT_RU_EN[item_lower])
            continue
            
        # Если не нашли, используем GoogleTranslator
        translator = GoogleTranslator(source='ru', target='en')
        try:
            translated = translator.translate(item)
            translated_list.append(translated.lower())
        except:
            # В случае ошибки возвращаем исходный текст
            translated_list.append(item_lower)
    
    return translated_list

async def translate_to_russian(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Translate English text or list of texts to Russian.
    Uses medical dictionary for common terms and GoogleTranslator as a fallback.
    Result will have the first letter of each word capitalized.
    
    Args:
        text: Single string or list of strings in English
        
    Returns:
        Translated text in Russian with capitalized first letter
    """
    if isinstance(text, str):
        # Проверяем в словаре сначала
        text_lower = text.lower()
        if text_lower in MED_DICT_EN_RU:
            return MED_DICT_EN_RU[text_lower].capitalize()
        
        # Если не нашли, используем GoogleTranslator
        translator = GoogleTranslator(source='en', target='ru')
        try:
            translated = translator.translate(text)
            return translated.capitalize()
        except:
            # В случае ошибки возвращаем исходный текст
            return text.capitalize()
    
    # For lists, translate each item and capitalize
    translated_list = []
    for item in text:
        # Проверяем в словаре сначала
        item_lower = item.lower()
        if item_lower in MED_DICT_EN_RU:
            translated_list.append(MED_DICT_EN_RU[item_lower].capitalize())
            continue
            
        # Если не нашли, используем GoogleTranslator
        translator = GoogleTranslator(source='en', target='ru')
        try:
            translated = translator.translate(item)
            translated_list.append(translated.capitalize())
        except:
            # В случае ошибки возвращаем исходный текст
            translated_list.append(item.capitalize())
    
    return translated_list