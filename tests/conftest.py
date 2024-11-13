import asyncio
import pytest
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models.base import Base, TimestampedBase  # Importáljuk mindkét base osztályt
from app.models.user import User
from app.models.url import URL
from app.db.session import get_db

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/test_urlshortener"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True  # Debug céljából bekapcsoljuk a SQL logolást
)

# Session factory
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get test database session."""
    # Először töröljük és létrehozzuk a táblákat
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # Létrehozunk egy új session-t
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
    
    # Cleanup után töröljük a táblákat
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def client(db_session) -> Generator:
    """Create test client."""
    def override_get_db():
        return db_session
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()