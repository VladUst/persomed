from pydantic import BaseModel, Field


class MedicalDocumentBase(BaseModel):
    name: str = Field(description="Document name")
    type: str = Field(description="Document type")
    date: str = Field(description="Document date")


class MedicalDocumentCreate(MedicalDocumentBase):
    pass


class MedicalDocument(MedicalDocumentBase):
    id: int = Field(description="Unique identifier")
    
    class Config:
        from_attributes = True 