from sqlalchemy.ext.asyncio import AsyncSession

from src.models.medical_documents import OtherDoc
from src.repositories.base_repository import BaseRepository


class OtherDocRepository(BaseRepository[OtherDoc]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OtherDoc) 