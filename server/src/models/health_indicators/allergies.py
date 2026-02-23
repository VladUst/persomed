from src.database import Base
from src.models.health_indicators.base import HealthIndicatorBase


class AllergiesInfo(Base, HealthIndicatorBase):
    __tablename__ = "allergies_info" 