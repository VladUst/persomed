from typing import Optional
from pydantic import Field

from src.schemas.health_indicators.base import HealthIndicatorBase


class LaboratoryInfoBase(HealthIndicatorBase):
    value: float = Field(description="Числовое значение показателя")


class LaboratoryInfoCreate(LaboratoryInfoBase):
    pass


class LaboratoryInfo(LaboratoryInfoBase):
    id: int
    target_reached: Optional[bool] = None
    
    class Config:
        from_attributes = True 