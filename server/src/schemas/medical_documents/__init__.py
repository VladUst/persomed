from src.schemas.medical_documents.base import MedicalDocumentBase, MedicalDocumentCreate, MedicalDocument
from src.schemas.medical_documents.analyzes import AnalyzesDocCreate, AnalyzesDoc
from src.schemas.medical_documents.other import OtherDocCreate, OtherDoc
from src.schemas.medical_documents.diseases_history import (
    DiseasesHistoryDocBase, DiseasesHistoryDocCreate, DiseasesHistoryDoc,
    DiseasesHistoryDocMetaInfo, DiseasesHistoryDocSections,
    DiseasesHistoryDocDetailsBase, DiseasesHistoryDocDetailsCreate, 
    DiseasesHistoryDocDetails, DiseasesHistoryDocWithDetails
)
from src.schemas.medical_documents.recommendations import RecommendationsDocBase, RecommendationsDocCreate, RecommendationsDoc

__all__ = [
    "MedicalDocumentBase", "MedicalDocumentCreate", "MedicalDocument",
    "AnalyzesDocCreate", "AnalyzesDoc",
    "OtherDocCreate", "OtherDoc",
    "DiseasesHistoryDocBase", "DiseasesHistoryDocCreate", "DiseasesHistoryDoc",
    "DiseasesHistoryDocMetaInfo", "DiseasesHistoryDocSections",
    "DiseasesHistoryDocDetailsBase", "DiseasesHistoryDocDetailsCreate", 
    "DiseasesHistoryDocDetails", "DiseasesHistoryDocWithDetails",
    "RecommendationsDocBase", "RecommendationsDocCreate", "RecommendationsDoc"
] 