from typing import List, Dict, Any, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models import (
    GeneralInfo,
    DetailedInfo,
    PreventiveInfo,
    AllergiesInfo,
    FamilyHistoryInfo,
    LifestyleInfo
)
from src.repositories.base_repository import BaseRepository


class HealthIndicatorRepository(BaseRepository):
    """
    Базовый класс репозитория для показателей здоровья
    """
    
    def _calculate_target_reached(self, data: Dict[str, Any]) -> Optional[bool]:
        """
        Рассчитывает достижение целевого показателя на основе данных.
        
        Возвращает:
            - True, если value в пределах [target_level_min, target_level_max]
            - False, если value вне пределов или невозможно определить
            - None, если необходимые значения отсутствуют
        """
        value = data.get('value')
        target_min = data.get('target_level_min')
        target_max = data.get('target_level_max')
        
        # Если нет целевых показателей, результат неопределен
        if target_min is None or target_max is None:
            return None
        
        try:
            # Для DetailedInfo value уже float, для других типов нужно преобразовать
            if isinstance(value, (int, float)):
                float_value = float(value)
            else:
                float_value = float(value)
            
            return target_min <= float_value <= target_max
        except (ValueError, TypeError):
            return False
    
    async def create(self, data: Dict[str, Any]) -> Any:
        """
        Создает новую запись с расчетом target_reached
        """
        # Расчет target_reached
        target_reached = self._calculate_target_reached(data)
        if target_reached is not None:
            data['target_reached'] = target_reached
        
        return await super().create(data)
    
    async def update(self, id: str, data: Dict[str, Any]) -> Any:
        """
        Обновляет запись с перерасчетом target_reached
        """
        # Получаем существующую запись
        item = await self.get_by_id(id)
        if not item:
            return None
        
        # Объединяем существующие данные с новыми для полного расчета
        full_data = item.__dict__.copy()
        full_data.update(data)
        
        # Пересчитываем target_reached
        target_reached = self._calculate_target_reached(full_data)
        if target_reached is not None:
            data['target_reached'] = target_reached
        
        return await super().update(id, data)


class GeneralInfoRepository(HealthIndicatorRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(GeneralInfo, session)


class DetailedInfoRepository(HealthIndicatorRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(DetailedInfo, session)


class PreventiveInfoRepository(HealthIndicatorRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(PreventiveInfo, session)


class AllergiesInfoRepository(HealthIndicatorRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(AllergiesInfo, session)


class FamilyHistoryInfoRepository(HealthIndicatorRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(FamilyHistoryInfo, session)


class LifestyleInfoRepository(HealthIndicatorRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(LifestyleInfo, session) 