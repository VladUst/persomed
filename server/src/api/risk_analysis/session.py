from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import new_session


async def get_session():
    """
    Зависимость для получения сессии базы данных в эндпоинтах API риск-анализа.
    
    Returns:
        AsyncSession: Сессия базы данных.
    """
    async with new_session() as session:
        yield session 