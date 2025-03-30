from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Model
from src.models.medical_documents.base import MedicalDocumentBase


class RecommendationsDoc(Model, MedicalDocumentBase):
    __tablename__ = "recommendations_docs"
    
    specialty: Mapped[str] = mapped_column(String) 