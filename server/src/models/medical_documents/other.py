from src.database import Model
from src.models.medical_documents.base import MedicalDocumentBase


class OtherDoc(Model, MedicalDocumentBase):
    __tablename__ = "other_docs" 