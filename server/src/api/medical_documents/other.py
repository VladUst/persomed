from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_depends import get_async_db
from src.schemas.medical_documents import OtherDoc, OtherDocCreate
from src.repositories.medical_documents import OtherDocRepository

# Создаем роутер для прочих документов
other_router = APIRouter(
    prefix="/other",
    tags=["Другие документы"]
)

@other_router.get("/", response_model=List[OtherDoc], summary="Получить все прочие документы")
async def get_all_other_docs(patient_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Получение всех прочих медицинских документов.
    
    Возвращает список всех прочих медицинских документов.
    """
    repository = OtherDocRepository(db)
    return await repository.get_all_by_patient(patient_id)


@other_router.get("/{id}", response_model=OtherDoc, summary="Получить документ по ID")
async def get_other_doc(patient_id: int, id: int, db: AsyncSession = Depends(get_async_db)):
    repository = OtherDocRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Документ с ID {id} не найден")
    return item


@other_router.post("/", response_model=OtherDoc, status_code=status.HTTP_201_CREATED, summary="Создать документ")
async def create_other_doc(
    patient_id: int,
    data: OtherDocCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Создание нового прочего медицинского документа.
    
    - **name**: Название документа
    - **type**: Тип документа
    - **date**: Дата документа
    
    Возвращает созданный прочий документ с присвоенным ID.
    """
    repository = OtherDocRepository(db)
    return await repository.create({**data.model_dump(), "patient_id": patient_id})


@other_router.put("/{id}", response_model=OtherDoc, summary="Обновить документ")
async def update_other_doc(patient_id: int, id: int, data: OtherDocCreate, db: AsyncSession = Depends(get_async_db)):
    repository = OtherDocRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Документ с ID {id} не найден")
    return await repository.update(id, data.model_dump())


@other_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить документ")
async def delete_other_doc(patient_id: int, id: int, db: AsyncSession = Depends(get_async_db)):
    repository = OtherDocRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Документ с ID {id} не найден")
    await repository.delete(id) 