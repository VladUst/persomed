from src.database import Model
from src.models.health_indicators.base import HealthIndicatorBase


class PreventiveInfo(Model, HealthIndicatorBase):
    __tablename__ = "preventive_info" 