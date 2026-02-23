from src.database import Base
from src.models.health_indicators.base import HealthIndicatorBase


class LifestyleInfo(Base, HealthIndicatorBase):
    __tablename__ = "lifestyle_info" 