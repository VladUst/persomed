from sqlalchemy.ext.asyncio import AsyncSession

from src.models.health_indicators import DetailedInfo
from src.repositories.health_indicators.base import HealthIndicatorRepository


class DetailedInfoRepository(HealthIndicatorRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(DetailedInfo, session) 