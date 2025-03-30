from src.database import Model
from src.models.medical_documents.base import MedicalDocumentBase


class AnalyzesDoc(Model, MedicalDocumentBase):
    __tablename__ = "analyzes_docs" 