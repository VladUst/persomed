from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from src.database import Base
from src.models.medical_documents.base import MedicalDocumentBase


class RecommendationsDoc(Base, MedicalDocumentBase):
    __tablename__ = "recommendations_docs"
    
    specialty: Mapped[str] = mapped_column(String)
    
    # Relationship with details
    details: Mapped["RecommendationsDocDetails"] = relationship(
        "RecommendationsDocDetails", 
        back_populates="document", 
        cascade="all, delete-orphan",
        uselist=False,
        foreign_keys="RecommendationsDocDetails.document_id"
    )


class RecommendationsDocDetails(Base):
    __tablename__ = "recommendations_doc_details"
    
    id: Mapped[int] = mapped_column(ForeignKey("recommendations_docs.id", ondelete="CASCADE"), primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("recommendations_docs.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String)
    
    # Meta information
    icd_code: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    doctor: Mapped[str] = mapped_column(String)
    specialty: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    clinic_name: Mapped[str] = mapped_column(String)
    
    # Sections
    instructions: Mapped[str] = mapped_column(String)
    
    # Relationship with document
    document: Mapped[RecommendationsDoc] = relationship(
        "RecommendationsDoc", 
        back_populates="details",
        foreign_keys=[document_id]
    ) 