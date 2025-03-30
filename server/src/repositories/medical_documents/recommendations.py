from sqlalchemy.ext.asyncio import AsyncSession

from src.models.medical_documents import RecommendationsDoc
from src.repositories.base_repository import BaseRepository


class RecommendationsDocRepository(BaseRepository[RecommendationsDoc]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RecommendationsDoc) 