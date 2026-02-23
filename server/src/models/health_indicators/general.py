from src.database import Base
from src.models.health_indicators.base import HealthIndicatorBase


class GeneralInfo(Base, HealthIndicatorBase):
    __tablename__ = "general_info" 