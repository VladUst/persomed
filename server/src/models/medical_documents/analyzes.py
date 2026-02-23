from src.database import Base
from src.models.medical_documents.base import MedicalDocumentBase


class AnalyzesDoc(Base, MedicalDocumentBase):
    __tablename__ = "analyzes_docs" 