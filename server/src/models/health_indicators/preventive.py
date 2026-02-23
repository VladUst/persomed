from src.database import Base
from src.models.health_indicators.base import HealthIndicatorBase


class PreventiveInfo(Base, HealthIndicatorBase):
    __tablename__ = "preventive_info" 