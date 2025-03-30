from src.repositories.medical_documents.analyzes import AnalyzesDocRepository
from src.repositories.medical_documents.other import OtherDocRepository
from src.repositories.medical_documents.diseases_history import DiseasesHistoryDocRepository, DiseasesHistoryDocDetailsRepository
from src.repositories.medical_documents.recommendations import RecommendationsDocRepository

__all__ = [
    "AnalyzesDocRepository",
    "OtherDocRepository",
    "DiseasesHistoryDocRepository",
    "DiseasesHistoryDocDetailsRepository",
    "RecommendationsDocRepository"
] 