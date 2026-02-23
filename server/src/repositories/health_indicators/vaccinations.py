from sqlalchemy.ext.asyncio import AsyncSession

from src.models.health_indicators import VaccinationsInfo
from src.repositories.health_indicators.base import HealthIndicatorRepository


class VaccinationsInfoRepository(HealthIndicatorRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, VaccinationsInfo) 