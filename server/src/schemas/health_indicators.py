from typing import List, Optional
from pydantic import BaseModel, Field


# Base schemas for health indicators with common fields
class HealthIndicatorBase(BaseModel):
    name: str = Field(description="Indicator name")
    orig_name: str = Field(description="Original indicator name")
    value: Optional[str] = Field(None, description="Indicator value")
    unit: Optional[str] = Field(None, description="Measurement unit")
    date: Optional[str] = Field(None, description="Date of measurement")


class HealthIndicatorCreate(HealthIndicatorBase):
    pass


class HealthIndicator(HealthIndicatorBase):
    id: int = Field(description="Unique identifier")
    
    class Config:
        from_attributes = True


# Detailed info with additional fields
class DetailedInfoBase(HealthIndicatorBase):
    unit: str = Field(description="Measurement unit")
    value: Optional[float] = Field(None, description="Indicator value")
    target_level_min: float = Field(description="Minimum target level")
    target_level_max: float = Field(description="Maximum target level")


class DetailedInfoCreate(DetailedInfoBase):
    pass


class DetailedInfo(DetailedInfoBase):
    id: int = Field(description="Unique identifier")
    target_reached: Optional[bool] = Field(None, description="Whether target level is reached")
    
    class Config:
        from_attributes = True


# Specific schemas for each health indicator type
class GeneralInfoCreate(HealthIndicatorCreate):
    pass


class GeneralInfo(HealthIndicator):
    pass


class PreventiveInfoCreate(HealthIndicatorCreate):
    pass


class PreventiveInfo(HealthIndicator):
    pass


class AllergiesInfoCreate(HealthIndicatorCreate):
    pass


class AllergiesInfo(HealthIndicator):
    pass


class FamilyHistoryInfoCreate(HealthIndicatorCreate):
    pass


class FamilyHistoryInfo(HealthIndicator):
    pass


class LifestyleInfoCreate(HealthIndicatorCreate):
    pass


class LifestyleInfo(HealthIndicator):
    pass 