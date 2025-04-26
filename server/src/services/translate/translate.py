from deep_translator import GoogleTranslator
from typing import List, Union

async def translate_to_english(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Translate Russian text or list of texts to English.
    Result will be converted to lowercase to ensure case insensitivity.
    
    Args:
        text: Single string or list of strings in Russian
        
    Returns:
        Translated text in English, all lowercase
    """
    translator = GoogleTranslator(source='ru', target='en')
    
    if isinstance(text, str):
        translated = translator.translate(text)
        return translated.lower()
    
    # For lists, translate each item and convert to lowercase
    translated_list = []
    for item in text:
        translated = translator.translate(item)
        translated_list.append(translated.lower())
    
    return translated_list

async def translate_to_russian(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Translate English text or list of texts to Russian.
    Result will have the first letter of each word capitalized.
    
    Args:
        text: Single string or list of strings in English
        
    Returns:
        Translated text in Russian with capitalized first letter
    """
    translator = GoogleTranslator(source='en', target='ru')
    
    if isinstance(text, str):
        translated = translator.translate(text)
        return translated.capitalize()
    
    # For lists, translate each item and capitalize
    translated_list = []
    for item in text:
        translated = translator.translate(item)
        translated_list.append(translated.capitalize())
    
    return translated_list
