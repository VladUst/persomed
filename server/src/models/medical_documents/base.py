from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class MedicalDocumentBase(Base):
    """Базовый класс для всех медицинских документов"""
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String) 