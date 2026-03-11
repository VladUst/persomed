from typing import Optional
from sqlalchemy import String, Boolean, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class HealthIndicatorBase(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String)
    canonical_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    value: Mapped[str] = mapped_column(String)
    unit: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    target_level_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    target_level_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    target_reached: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True) 