from typing import Optional
from pydantic import BaseModel, Field


# Base schemas for medical documents with common fields
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


# Disease history document with ICD code
class DiseasesHistoryDocBase(MedicalDocumentBase):
    icd_code: str = Field(description="ICD code of the disease")


class DiseasesHistoryDocCreate(DiseasesHistoryDocBase):
    pass


class DiseasesHistoryDoc(DiseasesHistoryDocBase):
    id: int = Field(description="Unique identifier")
    
    class Config:
        from_attributes = True


# Recommendations document with specialty
class RecommendationsDocBase(MedicalDocumentBase):
    specialty: str = Field(description="Doctor specialty")


class RecommendationsDocCreate(RecommendationsDocBase):
    pass


class RecommendationsDoc(RecommendationsDocBase):
    id: int = Field(description="Unique identifier")
    
    class Config:
        from_attributes = True


# Analyses document
class AnalyzesDocCreate(MedicalDocumentCreate):
    pass


class AnalyzesDoc(MedicalDocument):
    pass


# Other documents
class OtherDocCreate(MedicalDocumentCreate):
    pass


class OtherDoc(MedicalDocument):
    pass


# Diseases history document meta information
class DiseasesHistoryDocMetaInfo(BaseModel):
    icd_code: str = Field(description="ICD code of the disease")
    diagnosis_date: str = Field(description="Date of diagnosis")
    doctor: str = Field(description="Doctor name")
    specialty: str = Field(description="Doctor specialty")
    nosology: str = Field(description="Nosology")
    disease_type: str = Field(description="Disease type")
    clinic_name: str = Field(description="Clinic name")


# Diseases history document sections
class DiseasesHistoryDocSections(BaseModel):
    anamnesis: str = Field(description="Patient anamnesis")
    clinical_findings: str = Field(description="Clinical findings")
    diagnosis: str = Field(description="Diagnosis")
    treatment_plan: str = Field(description="Treatment plan")
    conclusion: str = Field(description="Conclusion")


# Disease history document details
class DiseasesHistoryDocDetailsBase(BaseModel):
    title: str = Field(description="Document title")
    meta: DiseasesHistoryDocMetaInfo = Field(description="Document meta information")
    sections: DiseasesHistoryDocSections = Field(description="Document sections")


class DiseasesHistoryDocDetailsCreate(DiseasesHistoryDocDetailsBase):
    document_id: int = Field(description="ID of the related document")


class DiseasesHistoryDocDetails(DiseasesHistoryDocDetailsBase):
    id: int = Field(description="Unique identifier")
    document_id: int = Field(description="ID of the related document")
    
    class Config:
        from_attributes = True


# Combined disease history document with details for direct API response
class DiseasesHistoryDocWithDetails(DiseasesHistoryDoc):
    details: Optional[DiseasesHistoryDocDetails] = Field(None, description="Document details") 