from src.schemas.health_indicators import (
    GeneralInfo, GeneralInfoCreate,
    DetailedInfo, DetailedInfoCreate,
    PreventiveInfo, PreventiveInfoCreate,
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
from src.schemas.tasks import STaskAdd, STask, STaskId
from src.schemas.text_process import MedicalTextRequest, NamedEntity, TextProcessingResponse

__all__ = [
    # Health indicators
    "GeneralInfo", "GeneralInfoCreate",
    "DetailedInfo", "DetailedInfoCreate",
    "PreventiveInfo", "PreventiveInfoCreate",
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
    
    # Tasks
    "STaskAdd", "STask", "STaskId",
    
    # Text Processing
    "MedicalTextRequest", "NamedEntity", "TextProcessingResponse"
] 