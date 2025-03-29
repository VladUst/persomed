from src.database import Model
from src.models.health_indicators.base import HealthIndicatorBase


class AllergiesInfo(Model, HealthIndicatorBase):
    __tablename__ = "allergies_info" 