from typing import List, Optional
from pydantic import BaseModel, Field


# Base health indicator model
class HealthIndicatorBase(BaseModel):
    name: str = Field(description="Название показателя")
    canonical_name: Optional[str] = Field(None, description="Каноническое название показателя")
    value: str = Field(description="Значение показателя")
    unit: Optional[str] = Field(None, description="Единица измерения")
    date: Optional[str] = Field(None, description="Дата измерения")
    target_level_min: Optional[float] = Field(None, description="Минимальное целевое значение")
    target_level_max: Optional[float] = Field(None, description="Максимальное целевое значение")


# Base health indicator for responses
class HealthIndicatorResponse(HealthIndicatorBase):
    id: int
    target_reached: Optional[bool] = None
    
    class Config:
        from_attributes = True


# General info
class GeneralInfoCreate(HealthIndicatorBase):
    pass


class GeneralInfo(HealthIndicatorResponse):
    pass


# Detailed info with special value field
class DetailedInfoBase(BaseModel):
    name: str = Field(description="Название показателя")
    canonical_name: Optional[str] = Field(None, description="Каноническое название показателя")
    value: float = Field(description="Числовое значение показателя")
    unit: Optional[str] = Field(None, description="Единица измерения")
    date: Optional[str] = Field(None, description="Дата измерения")
    target_level_min: Optional[float] = Field(None, description="Минимальное целевое значение")
    target_level_max: Optional[float] = Field(None, description="Максимальное целевое значение")


class DetailedInfoCreate(DetailedInfoBase):
    pass


class DetailedInfo(DetailedInfoBase):
    id: int
    target_reached: Optional[bool] = None
    
    class Config:
        from_attributes = True


# Preventive info
class PreventiveInfoCreate(HealthIndicatorBase):
    pass


class PreventiveInfo(HealthIndicatorResponse):
    pass


# Allergies info
class AllergiesInfoCreate(HealthIndicatorBase):
    pass


class AllergiesInfo(HealthIndicatorResponse):
    pass


# Family history info
class FamilyHistoryInfoCreate(HealthIndicatorBase):
    pass


class FamilyHistoryInfo(HealthIndicatorResponse):
    pass


# Lifestyle info
class LifestyleInfoCreate(HealthIndicatorBase):
    pass


class LifestyleInfo(HealthIndicatorResponse):
    pass 