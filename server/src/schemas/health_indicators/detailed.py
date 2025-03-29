from typing import Optional
from pydantic import BaseModel, Field


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