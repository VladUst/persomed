from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.health_indicators import GeneralInfoRepository, DetailedInfoRepository
from src.repositories.medical_documents import DiseasesHistoryDocRepository


async def find_abnormal_health_indicators(session: AsyncSession):
    """
    Находит показатели здоровья, выходящие за рамки норм.
    
    Args:
        session: Асинхронная сессия базы данных
        
    Returns:
        dict: Словарь с двумя массивами показателей:
              - low_level: показатели ниже нормы
              - high_level: показатели выше нормы
    """
    # Получаем общие показатели здоровья
    general_repo = GeneralInfoRepository(session)
    general_indicators = await general_repo.get_all()
    
    # Получаем детальные показатели здоровья
    detailed_repo = DetailedInfoRepository(session)
    detailed_indicators = await detailed_repo.get_all()
    
    # Объединяем все показатели
    all_indicators = general_indicators + detailed_indicators
    
    # Фильтруем показатели, у которых target_reached=False
    abnormal_indicators = [ind for ind in all_indicators if ind.target_reached is False]
    
    # Разделяем на показатели ниже нормы и выше нормы
    low_level_indicators = []
    high_level_indicators = []
    
    for indicator in abnormal_indicators:
        try:
            value = float(indicator.value)
            # Если значение ниже минимальной нормы
            if indicator.target_level_min is not None and value < indicator.target_level_min:
                low_level_indicators.append(indicator.name)
            # Если значение выше максимальной нормы
            elif indicator.target_level_max is not None and value > indicator.target_level_max:
                high_level_indicators.append(indicator.name)
        except (ValueError, TypeError):
            # Если значение не числовое, пропускаем
            continue
    
    return {
        "low_level": low_level_indicators,
        "high_level": high_level_indicators
    }


async def find_chronic_diseases(session: AsyncSession):
    """
    Находит хронические заболевания из истории болезней.
    
    Args:
        session: Асинхронная сессия базы данных
        
    Returns:
        list: Список хронических заболеваний
    """
    # Получаем историю болезней
    disease_repo = DiseasesHistoryDocRepository(session)
    disease_histories = await disease_repo.get_all_with_details()
    
    # Фильтруем хронические заболевания
    chronic_diseases = []
    
    for history in disease_histories:
        # Проверяем тип заболевания в основном объекте
        if history.type and history.type.lower() == "хроническое":
            chronic_diseases.append(history.name)
    
    return chronic_diseases


async def get_risk_factors(session: AsyncSession):
    """
    Получает все факторы риска по категориям.
    
    Args:
        session: Асинхронная сессия базы данных
        
    Returns:
        dict: Словарь с факторами риска по категориям
    """
    # Получаем текущую дату
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Получаем показатели, выходящие за нормы
    abnormal_indicators = await find_abnormal_health_indicators(session)
    
    # Получаем хронические заболевания
    chronic_diseases = await find_chronic_diseases(session)
    
    # Формируем текстовое описание для каждой категории
    low_level_info = "Пониженный уровень у показателей: " + ", ".join(abnormal_indicators["low_level"]) if abnormal_indicators["low_level"] else "Показателей с пониженным уровнем не обнаружено"
    
    high_level_info = "Повышенный уровень у показателей: " + ", ".join(abnormal_indicators["high_level"]) if abnormal_indicators["high_level"] else "Показателей с повышенным уровнем не обнаружено"
    
    chronic_info = "Хронические заболевания: " + ", ".join(chronic_diseases) if chronic_diseases else "Хронических заболеваний не обнаружено"
    
    return {
        "low_level": {
            "info": low_level_info,
            "source": "Сервис анализа отклонений показателей от норм",
            "date": current_date
        },
        "high_level": {
            "info": high_level_info,
            "source": "Сервис анализа отклонений показателей от норм",
            "date": current_date
        },
        "chronical": {
            "info": chronic_info,
            "source": "Сервис анализа хронических заболеваний",
            "date": current_date
        }
    }
