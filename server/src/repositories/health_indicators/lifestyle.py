from sqlalchemy.ext.asyncio import AsyncSession

from src.models.health_indicators import LifestyleInfo
from src.repositories.health_indicators.base import HealthIndicatorRepository


class LifestyleInfoRepository(HealthIndicatorRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(LifestyleInfo, session) 