from sqlalchemy.ext.asyncio import AsyncSession

from src.models.health_indicators import AllergiesInfo
from src.repositories.health_indicators.base import HealthIndicatorRepository


class AllergiesInfoRepository(HealthIndicatorRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AllergiesInfo) 