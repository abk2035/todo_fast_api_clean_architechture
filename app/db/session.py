from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Création du moteur async SQLAlchemy via asyncpg
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI.replace("postgresql+psycopg", "postgresql+asyncpg"),
    future=True,
)

# Factory de sessions asynchrones
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """Dépendance FastAPI pour fournir une session DB asynchrone par requête."""
    async with AsyncSessionLocal() as session:
        yield session
