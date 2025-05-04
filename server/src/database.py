from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("sqlite+aiosqlite:///persomed.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


async def create_tables():
    # https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-core
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

async def recreate_tables():
    """
    Удаляет и заново создает все таблицы в базе данных.
    ВНИМАНИЕ: Это приведет к потере всех данных.
    Используйте только при необходимости полного сброса базы данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
        await conn.run_sync(Model.metadata.create_all)
    print("База данных успешно пересоздана")