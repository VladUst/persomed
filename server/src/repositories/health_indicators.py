from sqlalchemy.ext.asyncio import AsyncSession

from src.models import (
    GeneralInfo, 
    DetailedInfo, 
    PreventiveInfo, 
    AllergiesInfo, 
    FamilyHistoryInfo, 
    LifestyleInfo
)
from src.repositories.base_repository import BaseRepository


class GeneralInfoRepository(BaseRepository[GeneralInfo]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, GeneralInfo)


class DetailedInfoRepository(BaseRepository[DetailedInfo]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DetailedInfo)
    
    async def create(self, data: dict) -> DetailedInfo:
        # Вычисляем target_reached на основе value и диапазона
        data["target_reached"] = self._calculate_target_reached(
            data.get("value"), 
            data.get("target_level_min"), 
            data.get("target_level_max")
        )
        return await super().create(data)
    
    async def update(self, id: int, data: dict) -> DetailedInfo:
        # Если обновляется value или границы диапазона, пересчитываем target_reached
        if "value" in data or "target_level_min" in data or "target_level_max" in data:
            # Получаем текущий объект, чтобы иметь полные данные для расчета
            current_item = await self.get_by_id(id)
            if current_item:
                # Определяем значения для расчета (новые или текущие)
                value = data.get("value", current_item.value)
                target_min = data.get("target_level_min", current_item.target_level_min)
                target_max = data.get("target_level_max", current_item.target_level_max)
                
                # Вычисляем target_reached
                data["target_reached"] = self._calculate_target_reached(value, target_min, target_max)
        
        return await super().update(id, data)
    
    def _calculate_target_reached(self, value, target_min, target_max):
        """
        Вычисляет target_reached на основе значения и диапазона.
        
        - Если value не определено, возвращает False
        - Если value определено и находится в диапазоне [target_min, target_max], возвращает True
        - Иначе возвращает False
        """
        if value is None:
            return False
            
        # Значение уже является float, поэтому преобразовывать не нужно
        return target_min <= value <= target_max


class PreventiveInfoRepository(BaseRepository[PreventiveInfo]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, PreventiveInfo)


class AllergiesInfoRepository(BaseRepository[AllergiesInfo]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AllergiesInfo)


class FamilyHistoryInfoRepository(BaseRepository[FamilyHistoryInfo]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, FamilyHistoryInfo)


class LifestyleInfoRepository(BaseRepository[LifestyleInfo]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, LifestyleInfo) 