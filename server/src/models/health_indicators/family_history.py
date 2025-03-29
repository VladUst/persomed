from src.database import Model
from src.models.health_indicators.base import HealthIndicatorBase


class FamilyHistoryInfo(Model, HealthIndicatorBase):
    __tablename__ = "family_history_info" 