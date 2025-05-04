import asyncio
from src.database import recreate_tables

async def main():
    await recreate_tables()
    print("База данных успешно пересоздана!")

if __name__ == "__main__":
    asyncio.run(main()) 