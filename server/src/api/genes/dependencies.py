"""Проверка пациента и единая блокировка загрузки, анализа и удаления."""

from collections.abc import AsyncIterator

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_depends import get_async_db
from src.repositories.patients import PatientRepository
from src.services.gene_analysis.errors import GeneAnalysisError
from src.services.gene_analysis.profile_storage import ProfileStorage


def get_profile_storage() -> ProfileStorage:
    return ProfileStorage()


async def require_patient(patient_id: int, db: AsyncSession = Depends(get_async_db)) -> None:
    if await PatientRepository(db).get_by_id(patient_id) is None:
        raise HTTPException(404, "Пациент не найден.")


async def locked_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_async_db),
    storage: ProfileStorage = Depends(get_profile_storage),
) -> AsyncIterator[ProfileStorage]:
    """Существование проверяется под lock, чтобы удаление не опередило загрузку."""
    try:
        with storage.lock(patient_id):
            await require_patient(patient_id, db)
            yield storage
    except GeneAnalysisError as exc:
        raise HTTPException(exc.status_code, str(exc)) from exc
    except OSError as exc:
        raise HTTPException(500, "Не удалось прочитать или сохранить данные генетического профиля.") from exc
