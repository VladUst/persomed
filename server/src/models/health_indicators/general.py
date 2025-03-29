from src.database import Model
from src.models.health_indicators.base import HealthIndicatorBase


class GeneralInfo(Model, HealthIndicatorBase):
    __tablename__ = "general_info" 