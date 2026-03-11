from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

async_engine = create_async_engine("sqlite+aiosqlite:///persomed.db")
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


# SQLite хранит FK-констрейнты в схеме ("FK enforcement is disabled by default"). Это сделано намеренно для обратной совместимости 
# (старые БД без FK продолжали работать после их добавления). PRAGMA foreign_keys=ON — официальный способ включить enforcement
@event.listens_for(async_engine.sync_engine, "connect")
def _enable_sqlite_fk(dbapi_connection, _connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Base(DeclarativeBase):
    pass

