from src.schemas.health_indicators import (
    GeneralInfo, GeneralInfoCreate,
    LaboratoryInfo, LaboratoryInfoCreate,
    VaccinationsInfo, VaccinationsInfoCreate,
    AllergiesInfo, AllergiesInfoCreate,
    FamilyHistoryInfo, FamilyHistoryInfoCreate,
    LifestyleInfo, LifestyleInfoCreate
)
from src.schemas.medical_documents import (
    MedicalDocumentBase, MedicalDocumentCreate, MedicalDocument,
    AnalyzesDocCreate, AnalyzesDoc,
    OtherDocCreate, OtherDoc,
    DiseasesHistoryDocBase, DiseasesHistoryDocCreate, DiseasesHistoryDoc,
    DiseasesHistoryDocMetaInfo, DiseasesHistoryDocSections,
    DiseasesHistoryDocDetailsBase, DiseasesHistoryDocDetailsCreate, 
    DiseasesHistoryDocDetails, DiseasesHistoryDocWithDetails,
    RecommendationsDocBase, RecommendationsDocCreate, RecommendationsDoc
)
from src.schemas.text_process import MedicalTextRequest, NamedEntity, TextProcessingResponse
from src.schemas.patient_status import PatientStatusResponse
from src.schemas.risk_analysis.risk_analysis import RiskAnalysisResponse

__all__ = [
    # Health indicators
    "GeneralInfo", "GeneralInfoCreate",
    "LaboratoryInfo", "LaboratoryInfoCreate",
    "VaccinationsInfo", "VaccinationsInfoCreate",
    "AllergiesInfo", "AllergiesInfoCreate",
    "FamilyHistoryInfo", "FamilyHistoryInfoCreate",
    "LifestyleInfo", "LifestyleInfoCreate",
    
    # Medical documents
    "MedicalDocumentBase", "MedicalDocumentCreate", "MedicalDocument",
    "AnalyzesDocCreate", "AnalyzesDoc",
    "OtherDocCreate", "OtherDoc",
    "DiseasesHistoryDocBase", "DiseasesHistoryDocCreate", "DiseasesHistoryDoc",
    "DiseasesHistoryDocMetaInfo", "DiseasesHistoryDocSections",
    "DiseasesHistoryDocDetailsBase", "DiseasesHistoryDocDetailsCreate", 
    "DiseasesHistoryDocDetails", "DiseasesHistoryDocWithDetails",
    "RecommendationsDocBase", "RecommendationsDocCreate", "RecommendationsDoc",

    # Text Processing
    "MedicalTextRequest", "NamedEntity", "TextProcessingResponse",

    # Patient status
    "PatientStatusResponse",

    # Risk analysis
    "RiskAnalysisResponse"
] 