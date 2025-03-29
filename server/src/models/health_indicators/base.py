from typing import Optional
from sqlalchemy import String, Boolean, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

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