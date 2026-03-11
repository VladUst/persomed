from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_depends import get_async_db
from src.schemas.patients import PatientCreate, PatientUpdate, PatientResponse
from src.repositories.patients import PatientRepository

router = APIRouter(
    prefix="/patients",
    tags=["Пациенты"],
)


@router.get("/", response_model=List[PatientResponse], summary="Получить список всех пациентов")
async def get_all_patients(db: AsyncSession = Depends(get_async_db)):
    repository = PatientRepository(db)
    return await repository.get_all()


@router.get("/{patient_id}", response_model=PatientResponse, summary="Получить пациента по ID")
async def get_patient(patient_id: int, db: AsyncSession = Depends(get_async_db)):
    repository = PatientRepository(db)
    patient = await repository.get_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пациент с ID {patient_id} не найден")
    return patient


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED, summary="Создать пациента")
async def create_patient(data: PatientCreate, db: AsyncSession = Depends(get_async_db)):
    repository = PatientRepository(db)
    return await repository.create(data.model_dump())


@router.put("/{patient_id}", response_model=PatientResponse, summary="Обновить данные пациента")
async def update_patient(patient_id: int, data: PatientUpdate, db: AsyncSession = Depends(get_async_db)):
    repository = PatientRepository(db)
    patient = await repository.get_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пациент с ID {patient_id} не найден")
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    return await repository.update(patient_id, update_data)


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить пациента")
async def delete_patient(patient_id: int, db: AsyncSession = Depends(get_async_db)):
    repository = PatientRepository(db)
    patient = await repository.get_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пациент с ID {patient_id} не найден")
    await repository.delete(patient_id)
