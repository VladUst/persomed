from sqlalchemy.ext.asyncio import AsyncSession

from src.models.medical_documents import AnalyzesDoc
from src.repositories.base_repository import BaseRepository


class AnalyzesDocRepository(BaseRepository[AnalyzesDoc]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AnalyzesDoc) 