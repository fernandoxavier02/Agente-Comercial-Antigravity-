from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from functools import lru_cache
import os

Base = declarative_base()

# Engine é criado de forma lazy, não na importação
_engine = None
_session_factory = None

def get_database_url() -> str:
    """Pega DATABASE_URL de variável de ambiente ou usa default local."""
    return os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/estetica_agent")

def get_engine():
    """Cria engine de forma lazy (só quando necessário)."""
    global _engine
    if _engine is None:
        database_url = get_database_url()
        _engine = create_async_engine(
            database_url,
            echo=False,  # Desliga logs SQL em produção
            pool_pre_ping=True,  # Verifica conexão antes de usar
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
        )
    return _engine

def get_session_factory():
    """Cria session factory de forma lazy."""
    global _session_factory
    if _session_factory is None:
        _session_factory = sessionmaker(
            get_engine(), 
            class_=AsyncSession, 
            expire_on_commit=False
        )
    return _session_factory

async def get_db():
    """Dependency para FastAPI - cria sessão por request."""
    factory = get_session_factory()
    async with factory() as session:
        yield session

# Para compatibilidade com init_db.py
@property
def engine():
    return get_engine()
