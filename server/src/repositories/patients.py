from sqlalchemy.ext.asyncio import AsyncSession

from src.models.patients import Patient
from src.repositories.base_repository import BaseRepository


class PatientRepository(BaseRepository[Patient]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Patient)
