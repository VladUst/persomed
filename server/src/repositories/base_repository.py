from typing import Generic, List, Optional, Type, TypeVar, Dict, Any
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Model

T = TypeVar("T", bound=Model)


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model
    
    async def get_all(self) -> List[T]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()
    
    async def get_by_id(self, id: int) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalars().first()
    
    async def create(self, data: Dict[str, Any]) -> T:
        # ID will be automatically generated by the database
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def update(self, id: int, data: Dict[str, Any]) -> Optional[T]:
        await self.session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
        )
        await self.session.commit()
        return await self.get_by_id(id)
    
    async def delete(self, id: int) -> bool:
        result = await self.session.execute(
            delete(self.model)
            .where(self.model.id == id)
        )
        await self.session.commit()
        return result.rowcount > 0 