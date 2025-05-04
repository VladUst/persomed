from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.medical_documents import RecommendationsDoc, RecommendationsDocDetails
from src.repositories.base_repository import BaseRepository


class RecommendationsDocRepository(BaseRepository[RecommendationsDoc]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RecommendationsDoc)
    
    async def get_by_id_with_details(self, id: int) -> Optional[RecommendationsDoc]:
        """Get recommendations document with details"""
        result = await self.session.execute(
            select(RecommendationsDoc)
            .options(selectinload(RecommendationsDoc.details))
            .where(RecommendationsDoc.id == id)
        )
        return result.scalars().first()
    
    async def get_all_with_details(self):
        """Get all recommendations documents with details"""
        result = await self.session.execute(
            select(RecommendationsDoc)
            .options(selectinload(RecommendationsDoc.details))
        )
        return result.scalars().all()


class RecommendationsDocDetailsRepository(BaseRepository[RecommendationsDocDetails]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RecommendationsDocDetails)
    
    async def get_by_document_id(self, document_id: int) -> Optional[RecommendationsDocDetails]:
        """Get recommendations document details by document ID"""
        result = await self.session.execute(
            select(RecommendationsDocDetails)
            .where(RecommendationsDocDetails.document_id == document_id)
        )
        return result.scalars().first() 