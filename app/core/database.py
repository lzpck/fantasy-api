from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Para desenvolvimento local, use uma URL de exemplo
# Para produção no Render, configure a variável de ambiente DATABASE_URL
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://user:password@localhost/fantasy_db"
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    """Dependency para obter sessão do banco de dados"""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()