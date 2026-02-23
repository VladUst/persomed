from src.database import Base
from src.models.health_indicators.base import HealthIndicatorBase


class FamilyHistoryInfo(Base, HealthIndicatorBase):
    __tablename__ = "family_history_info" 