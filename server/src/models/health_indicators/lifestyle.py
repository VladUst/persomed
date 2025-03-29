from src.database import Model
from src.models.health_indicators.base import HealthIndicatorBase


class LifestyleInfo(Model, HealthIndicatorBase):
    __tablename__ = "lifestyle_info" 