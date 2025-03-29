from typing import List, Optional, Tuple
from sqlalchemy import String, Boolean, Float, JSON, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Model


# Базовый класс только для общих полей, не будет создавать таблицу
class HealthIndicatorBase:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    canonical_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    value: Mapped[str] = mapped_column(String)
    unit: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    target_level_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    target_level_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    target_reached: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)


# Конкретные реализации для каждого типа показателя
class GeneralInfo(Model, HealthIndicatorBase):
    __tablename__ = "general_info"


class DetailedInfo(Model, HealthIndicatorBase):
    __tablename__ = "detailed_info"
    
    # Переопределяем поле value для DetailedInfo как float
    value: Mapped[float] = mapped_column(Float)


class PreventiveInfo(Model, HealthIndicatorBase):
    __tablename__ = "preventive_info"


class AllergiesInfo(Model, HealthIndicatorBase):
    __tablename__ = "allergies_info"


class FamilyHistoryInfo(Model, HealthIndicatorBase):
    __tablename__ = "family_history_info"


class LifestyleInfo(Model, HealthIndicatorBase):
    __tablename__ = "lifestyle_info"


 