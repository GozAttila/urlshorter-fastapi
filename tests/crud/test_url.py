import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_url, crud_user
from app.schemas.url import URLCreate
from app.schemas.user import UserCreate

pytestmark = pytest.mark.asyncio

async def test_create_url(db_session: AsyncSession):
    original_url = "https://example.com"
    url_in = URLCreate(
        original_url=original_url,
        slug="test123"
    )
    url = await crud_url.url.create(db_session, obj_in=url_in)
    
    assert url.original_url.rstrip('/') == original_url
    assert url.slug == "test123"
    assert url.visits == 0

async def test_get_url(db_session: AsyncSession):
    url_in = URLCreate(
        original_url="https://example.com",
        slug="test123"
    )
    url = await crud_url.url.create(db_session, obj_in=url_in)
    
    stored_url = await crud_url.url.get(db_session, id=url.id)
    assert stored_url
    assert url.original_url == stored_url.original_url
    assert url.slug == stored_url.slug

async def test_get_url_by_slug(db_session: AsyncSession):
    url_in = URLCreate(
        original_url="https://example.com",
        slug="test123"
    )
    url = await crud_url.url.create(db_session, obj_in=url_in)
    
    stored_url = await crud_url.url.get_by_slug(db_session, slug=url.slug)
    assert stored_url
    assert url.original_url == stored_url.original_url
    assert url.slug == stored_url.slug

async def test_increment_visits(db_session: AsyncSession):
    url_in = URLCreate(
        original_url="https://example.com",
        slug="test123"
    )
    url = await crud_url.url.create(db_session, obj_in=url_in)
    
    assert url.visits == 0
    updated_url = await crud_url.url.increment_visits(db_session, url=url)
    assert updated_url.visits == 1

async def test_get_user_urls(db_session: AsyncSession):
    # Create user
    user_in = UserCreate(
        email="test@example.com",
        password="testpass123"
    )
    user = await crud_user.user.create(db_session, obj_in=user_in)
    
    # Create URLs for user
    url1_in = URLCreate(
        original_url="https://example1.com",
        slug="test1"
    )
    url2_in = URLCreate(
        original_url="https://example2.com",
        slug="test2"
    )
    
    url1 = await crud_url.url.create(db_session, obj_in=url1_in)
    url2 = await crud_url.url.create(db_session, obj_in=url2_in)
    
    # Set user_id for URLs
    url1.user_id = user.id
    url2.user_id = user.id
    db_session.add(url1)
    db_session.add(url2)
    await db_session.commit()
    
    # Get user's URLs
    user_urls = await crud_url.url.get_user_urls(db_session, user_id=user.id)
    assert len(user_urls) == 2
    assert all(url.user_id == user.id for url in user_urls) 