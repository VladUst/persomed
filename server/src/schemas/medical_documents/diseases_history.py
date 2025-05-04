from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, model_validator
from src.schemas.medical_documents.base import MedicalDocumentBase, MedicalDocument


# Disease history document with ICD code
class DiseasesHistoryDocBase(MedicalDocumentBase):
    icd_code: str = Field(description="ICD code of the disease")


class DiseasesHistoryDocCreate(DiseasesHistoryDocBase):
    pass


class DiseasesHistoryDoc(DiseasesHistoryDocBase):
    id: int = Field(description="Unique identifier")
    
    model_config = {
        "from_attributes": True
    }


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
    clinical_findings: Optional[str] = Field(None, description="Clinical findings")
    diagnosis: Optional[str] = Field(None, description="Diagnosis")
    treatment_plan: Optional[str] = Field(None, description="Treatment plan")
    conclusion: Optional[str] = Field(None, description="Conclusion")


# Disease history document details
class DiseasesHistoryDocDetailsBase(BaseModel):
    title: str = Field(description="Document title")
    meta: DiseasesHistoryDocMetaInfo = Field(description="Document meta information")
    sections: DiseasesHistoryDocSections = Field(description="Document sections")


class DiseasesHistoryDocDetailsCreate(DiseasesHistoryDocDetailsBase):
    pass


class DiseasesHistoryDocDetails(DiseasesHistoryDocDetailsBase):
    id: int = Field(description="Unique identifier")
    document_id: int = Field(description="ID of the related document")
    
    model_config = {
        "from_attributes": True
    }
    
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, data: Any) -> Dict[str, Any]:
        if hasattr(data, "__dict__") and not isinstance(data, dict):
            # Если это объект ORM, создаем вложенную структуру
            db_obj_dict = data.__dict__
            return {
                "id": db_obj_dict.get("id"),
                "document_id": db_obj_dict.get("document_id"),
                "title": db_obj_dict.get("title"),
                "meta": {
                    "icd_code": db_obj_dict.get("icd_code"),
                    "diagnosis_date": db_obj_dict.get("diagnosis_date"),
                    "doctor": db_obj_dict.get("doctor"),
                    "specialty": db_obj_dict.get("specialty"),
                    "nosology": db_obj_dict.get("nosology"),
                    "disease_type": db_obj_dict.get("disease_type"),
                    "clinic_name": db_obj_dict.get("clinic_name")
                },
                "sections": {
                    "anamnesis": db_obj_dict.get("anamnesis"),
                    "clinical_findings": db_obj_dict.get("clinical_findings"),
                    "diagnosis": db_obj_dict.get("diagnosis"),
                    "treatment_plan": db_obj_dict.get("treatment_plan"),
                    "conclusion": db_obj_dict.get("conclusion")
                }
            }
        return data


# Combined disease history document with details for direct API response
class DiseasesHistoryDocWithDetails(DiseasesHistoryDoc):
    details: Optional[DiseasesHistoryDocDetails] = Field(None, description="Document details") 