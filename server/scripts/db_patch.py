import os
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь импорта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Переопределяем engine с абсолютным путем
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.database import Model

# Абсолютный путь к файлу базы данных в корне проекта
db_path = os.path.join(project_root, "persomed.db")
db_uri = f"sqlite+aiosqlite:///{db_path}"

# Создаем новый engine с абсолютным путем
engine = create_async_engine(db_uri)
new_session = async_sessionmaker(engine, expire_on_commit=False)

# Функции для работы с БД
async def create_tables():
    # https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-core
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all) 