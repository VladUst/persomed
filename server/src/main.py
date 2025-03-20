from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.database import create_tables, delete_tables
from src.api import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)