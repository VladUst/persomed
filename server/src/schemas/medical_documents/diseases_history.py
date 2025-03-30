from typing import Optional
from pydantic import BaseModel, Field
from src.schemas.medical_documents.base import MedicalDocumentBase, MedicalDocument


# Disease history document with ICD code
class DiseasesHistoryDocBase(MedicalDocumentBase):
    icd_code: str = Field(description="ICD code of the disease")


class DiseasesHistoryDocCreate(DiseasesHistoryDocBase):
    pass


class DiseasesHistoryDoc(DiseasesHistoryDocBase):
    id: int = Field(description="Unique identifier")
    
    class Config:
        from_attributes = True


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