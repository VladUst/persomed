from typing import List, Optional, Tuple
from sqlalchemy import String, Boolean, Float, JSON, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Model


class GeneralInfo(Model):
    __tablename__ = "general_info"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    orig_name: Mapped[str] = mapped_column(String)
    value: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class DetailedInfo(Model):
    __tablename__ = "detailed_info"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    orig_name: Mapped[str] = mapped_column(String)
    unit: Mapped[str] = mapped_column(String)
    value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    date: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    target_reached: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    target_level_min: Mapped[float] = mapped_column(Float)
    target_level_max: Mapped[float] = mapped_column(Float)


class PreventiveInfo(Model):
    __tablename__ = "preventive_info"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    orig_name: Mapped[str] = mapped_column(String)
    value: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class AllergiesInfo(Model):
    __tablename__ = "allergies_info"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    orig_name: Mapped[str] = mapped_column(String)
    value: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class FamilyHistoryInfo(Model):
    __tablename__ = "family_history_info"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    orig_name: Mapped[str] = mapped_column(String)
    value: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class LifestyleInfo(Model):
    __tablename__ = "lifestyle_info"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    orig_name: Mapped[str] = mapped_column(String)
    value: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date: Mapped[Optional[str]] = mapped_column(String, nullable=True)


 