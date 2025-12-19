import asyncio
from app.core.database import get_engine, Base
from app import models

async def init_models():
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Banco de dados Recriado.")
    print(f"Colunas de Lead: {list(Base.metadata.tables['leads'].columns.keys())}")

if __name__ == "__main__":
    asyncio.run(init_models())
