from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column
from src.models.health_indicators.base import HealthIndicatorBase


class LaboratoryInfo(HealthIndicatorBase):
    __tablename__ = "detailed_info"
    
    value: Mapped[float] = mapped_column(Float) 