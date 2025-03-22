from src.schemas.health_indicators import (
    GeneralInfo, GeneralInfoCreate,
    DetailedInfo, DetailedInfoCreate,
    PreventiveInfo, PreventiveInfoCreate,
    AllergiesInfo, AllergiesInfoCreate,
    FamilyHistoryInfo, FamilyHistoryInfoCreate,
    LifestyleInfo, LifestyleInfoCreate
)

from src.schemas.medical_documents import (
    AnalyzesDoc, AnalyzesDocCreate,
    OtherDoc, OtherDocCreate,
    DiseasesHistoryDoc, DiseasesHistoryDocCreate,
    RecommendationsDoc, RecommendationsDocCreate,
    DiseasesHistoryDocDetails, DiseasesHistoryDocDetailsCreate,
    DiseasesHistoryDocWithDetails
)

__all__ = [
    # Health indicators
    "GeneralInfo", "GeneralInfoCreate",
    "DetailedInfo", "DetailedInfoCreate", 
    "PreventiveInfo", "PreventiveInfoCreate",
    "AllergiesInfo", "AllergiesInfoCreate",
    "FamilyHistoryInfo", "FamilyHistoryInfoCreate",
    "LifestyleInfo", "LifestyleInfoCreate",
    
    # Medical documents
    "AnalyzesDoc", "AnalyzesDocCreate",
    "OtherDoc", "OtherDocCreate",
    "DiseasesHistoryDoc", "DiseasesHistoryDocCreate",
    "RecommendationsDoc", "RecommendationsDocCreate",
    "DiseasesHistoryDocDetails", "DiseasesHistoryDocDetailsCreate",
    "DiseasesHistoryDocWithDetails"
] 