from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker, MappedAsDataclass


from app.core.config import settings

class Base(DeclarativeBase, MappedAsDataclass):
    pass

DATABASE_URI = settings.POSTGRES_URI
ASYNC_SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DATABASE_URI}"

async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL, 
    echo=False, 
    future=True
)

async def async_get_db() -> AsyncSession:
    async_session = sessionmaker(
        bind=async_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    async with async_session() as db:
        yield db
        await db.commit()
