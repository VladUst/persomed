from src.database import Base
from src.models.medical_documents.base import MedicalDocumentBase


class OtherDoc(Base, MedicalDocumentBase):
    __tablename__ = "other_docs" 