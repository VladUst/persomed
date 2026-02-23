from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column
from src.models.health_indicators.base import HealthIndicatorBase


class DetailedInfo(HealthIndicatorBase):
    __tablename__ = "detailed_info"
    
    # Переопределяем поле value для DetailedInfo как float
    value: Mapped[float] = mapped_column(Float) 