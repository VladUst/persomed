from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from src.database import Model
from src.models.medical_documents.base import MedicalDocumentBase


class DiseasesHistoryDoc(Model, MedicalDocumentBase):
    __tablename__ = "diseases_history_docs"
    
    icd_code: Mapped[str] = mapped_column(String)
    
    # Relationship with details
    details: Mapped["DiseasesHistoryDocDetails"] = relationship(
        "DiseasesHistoryDocDetails", 
        back_populates="document", 
        cascade="all, delete-orphan",
        uselist=False,
        foreign_keys="DiseasesHistoryDocDetails.document_id"
    )


class DiseasesHistoryDocDetails(Model):
    __tablename__ = "diseases_history_doc_details"
    
    id: Mapped[int] = mapped_column(ForeignKey("diseases_history_docs.id", ondelete="CASCADE"), primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("diseases_history_docs.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String)
    
    # Meta information
    icd_code: Mapped[str] = mapped_column(String)
    diagnosis_date: Mapped[str] = mapped_column(String)
    doctor: Mapped[str] = mapped_column(String)
    specialty: Mapped[str] = mapped_column(String)
    nosology: Mapped[str] = mapped_column(String)
    disease_type: Mapped[str] = mapped_column(String)
    clinic_name: Mapped[str] = mapped_column(String)
    
    # Sections
    anamnesis: Mapped[str] = mapped_column(String)
    clinical_findings: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    diagnosis: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    treatment_plan: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    conclusion: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Relationship with document
    document: Mapped[DiseasesHistoryDoc] = relationship(
        "DiseasesHistoryDoc", 
        back_populates="details",
        foreign_keys=[document_id]
    ) 