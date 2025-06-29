from contextlib import asynccontextmanager
import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

_DB_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://user:pass@postgres:5432/app"
)

_engine = create_async_engine(_DB_URL, pool_pre_ping=True, future=True)
SessionLocal = async_sessionmaker(_engine, expire_on_commit=False, autoflush=False)


@asynccontextmanager
async def db_session():
    """
    Async DB session context manager.

    Example:
        async with db_session() as db:
            db.add(obj)
    """
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
            # Note: No need to dispose the engine, SQLAlchemy handles that automatically.
            # _engine.dispose()  # Uncomment if you want to dispose the engine after each session.