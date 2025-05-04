from typing import Optional, Any, Dict
from pydantic import Field, BaseModel, model_validator
from src.schemas.medical_documents.base import MedicalDocumentBase, MedicalDocument


class RecommendationsDocBase(MedicalDocumentBase):
    specialty: str = Field(description="Doctor specialty")


class RecommendationsDocCreate(RecommendationsDocBase):
    pass


class RecommendationsDoc(RecommendationsDocBase):
    id: int = Field(description="Unique identifier")
    
    model_config = {
        "from_attributes": True
    }


# Recommendations document meta information
class RecommendationsDocMetaInfo(BaseModel):
    icd_code: str = Field(description="ICD code of the disease")
    date: str = Field(description="Date of recommendation")
    doctor: str = Field(description="Doctor name")
    specialty: str = Field(description="Doctor specialty")
    type: str = Field(description="Recommendation type")
    clinic_name: str = Field(description="Clinic name")


# Recommendations document sections
class RecommendationsDocSections(BaseModel):
    instructions: str = Field(description="Recommendation instructions")


# Recommendations document details
class RecommendationsDocDetailsBase(BaseModel):
    title: str = Field(description="Document title")
    meta: RecommendationsDocMetaInfo = Field(description="Document meta information")
    sections: RecommendationsDocSections = Field(description="Document sections")


class RecommendationsDocDetailsCreate(RecommendationsDocDetailsBase):
    pass


class RecommendationsDocDetails(RecommendationsDocDetailsBase):
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
                    "date": db_obj_dict.get("date"),
                    "doctor": db_obj_dict.get("doctor"),
                    "specialty": db_obj_dict.get("specialty"),
                    "type": db_obj_dict.get("type"),
                    "clinic_name": db_obj_dict.get("clinic_name")
                },
                "sections": {
                    "instructions": db_obj_dict.get("instructions")
                }
            }
        return data


# Combined recommendations document with details for direct API response
class RecommendationsDocWithDetails(RecommendationsDoc):
    details: Optional[RecommendationsDocDetails] = Field(None, description="Document details") 