from pydantic import Field
from src.schemas.medical_documents.base import MedicalDocumentBase, MedicalDocument


class RecommendationsDocBase(MedicalDocumentBase):
    specialty: str = Field(description="Doctor specialty")


class RecommendationsDocCreate(RecommendationsDocBase):
    pass


class RecommendationsDoc(RecommendationsDocBase):
    id: int = Field(description="Unique identifier")
    
    class Config:
        from_attributes = True 