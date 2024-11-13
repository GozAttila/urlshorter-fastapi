import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.user import User
from app.models.url import URL

pytestmark = pytest.mark.asyncio

async def test_create_user(db_session):
    user = User(
        email="test@example.com",
        hashed_password="testpass123",
        is_active=True
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.created_at is not None
    assert user.updated_at is not None

async def test_create_url(db_session):
    url = URL(
        original_url="https://example.com",
        slug="test123"
    )
    db_session.add(url)
    await db_session.flush()
    await db_session.refresh(url)
    
    assert url.id is not None
    assert url.original_url == "https://example.com"
    assert url.slug == "test123"
    assert url.visits == 0
    assert url.created_at is not None
    assert url.updated_at is not None

async def test_user_url_relationship(db_session):
    # Create user
    user = User(
        email="test@example.com",
        hashed_password="testpass123"
    )
    db_session.add(user)
    await db_session.flush()
    
    # Create URL for user
    url = URL(
        original_url="https://example.com",
        slug="test123",
        user_id=user.id
    )
    db_session.add(url)
    await db_session.flush()
    await db_session.refresh(url)
    
    # Test relationship
    assert url.user_id == user.id
    
    # Test backref
    stmt = (
        select(User)
        .options(selectinload(User.urls))
        .where(User.id == user.id)
    )
    result = await db_session.execute(stmt)
    db_user = result.scalar_one()
    
    # Explicit módon betöltjük a kapcsolódó objektumokat
    urls = db_user.urls
    assert len(urls) == 1
    assert urls[0].slug == "test123" 