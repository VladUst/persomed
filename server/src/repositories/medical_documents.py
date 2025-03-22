from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import (
    AnalyzesDoc,
    OtherDoc, 
    DiseasesHistoryDoc, 
    RecommendationsDoc,
    DiseasesHistoryDocDetails
)
from src.repositories.base_repository import BaseRepository


class AnalyzesDocRepository(BaseRepository[AnalyzesDoc]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AnalyzesDoc)


class OtherDocRepository(BaseRepository[OtherDoc]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OtherDoc)


class RecommendationsDocRepository(BaseRepository[RecommendationsDoc]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RecommendationsDoc)


class DiseasesHistoryDocRepository(BaseRepository[DiseasesHistoryDoc]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DiseasesHistoryDoc)
    
    async def get_by_id_with_details(self, id: str) -> Optional[DiseasesHistoryDoc]:
        """Get disease history document with details"""
        result = await self.session.execute(
            select(DiseasesHistoryDoc)
            .options(selectinload(DiseasesHistoryDoc.details))
            .where(DiseasesHistoryDoc.id == id)
        )
        return result.scalars().first()
    
    async def get_all_with_details(self):
        """Get all disease history documents with details"""
        result = await self.session.execute(
            select(DiseasesHistoryDoc)
            .options(selectinload(DiseasesHistoryDoc.details))
        )
        return result.scalars().all()


class DiseasesHistoryDocDetailsRepository(BaseRepository[DiseasesHistoryDocDetails]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DiseasesHistoryDocDetails)
    
    async def get_by_document_id(self, document_id: str) -> Optional[DiseasesHistoryDocDetails]:
        """Get document details by document ID"""
        result = await self.session.execute(
            select(DiseasesHistoryDocDetails)
            .where(DiseasesHistoryDocDetails.document_id == document_id)
        )
        return result.scalars().first() 