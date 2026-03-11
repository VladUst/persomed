from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    name: str = Field(description="Имя пациента")
    surname: str = Field(description="Фамилия пациента")
    age: int = Field(gt=0, lt=150, description="Возраст пациента")


class PatientUpdate(BaseModel):
    name: str | None = Field(None, description="Имя пациента")
    surname: str | None = Field(None, description="Фамилия пациента")
    age: int | None = Field(None, gt=0, lt=150, description="Возраст пациента")


class PatientResponse(PatientCreate):
    id: int = Field(description="Уникальный идентификатор пациента")

    class Config:
        from_attributes = True
