from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_depends import get_async_db
from src.schemas.medical_documents import AnalyzesDoc, AnalyzesDocCreate
from src.repositories.medical_documents import AnalyzesDocRepository


# Создаем роутер для документов по анализам
analyzes_router = APIRouter(
    prefix="/analyzes",
    tags=["Лабораторные и диагностические исследования"]
)


@analyzes_router.get("/", response_model=List[AnalyzesDoc], summary="Получить все документы анализов")
async def get_all_analyzes_docs(patient_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Получение всех документов анализов.
    
    Возвращает список всех документов анализов.
    """
    repository = AnalyzesDocRepository(db)
    return await repository.get_all_by_patient(patient_id)


@analyzes_router.get("/{id}", response_model=AnalyzesDoc, summary="Получить документ анализа по ID")
async def get_analyzes_doc(patient_id: int, id: int, db: AsyncSession = Depends(get_async_db)):
    repository = AnalyzesDocRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Документ анализа с ID {id} не найден")
    return item


@analyzes_router.post("/", response_model=AnalyzesDoc, status_code=status.HTTP_201_CREATED, summary="Создать документ с результатами анализов")
async def create_analyzes_doc(
    patient_id: int,
    data: AnalyzesDocCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Создание нового документа анализа.
    
    - **name**: Название документа
    - **type**: Тип документа
    - **date**: Дата документа
    
    Возвращает созданный документ анализа с присвоенным ID.
    """
    repository = AnalyzesDocRepository(db)
    return await repository.create({**data.model_dump(), "patient_id": patient_id})


@analyzes_router.put("/{id}", response_model=AnalyzesDoc, summary="Обновить документ анализа")
async def update_analyzes_doc(patient_id: int, id: int, data: AnalyzesDocCreate, db: AsyncSession = Depends(get_async_db)):
    repository = AnalyzesDocRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Документ анализа с ID {id} не найден")
    return await repository.update(id, data.model_dump())


@analyzes_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить документ анализа")
async def delete_analyzes_doc(patient_id: int, id: int, db: AsyncSession = Depends(get_async_db)):
    repository = AnalyzesDocRepository(db)
    item = await repository.get_by_id(id)
    if not item or item.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Документ анализа с ID {id} не найден")
    await repository.delete(id) 