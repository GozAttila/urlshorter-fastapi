import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_user
from app.schemas.user import UserCreate
from app.core.security import verify_password

pytestmark = pytest.mark.asyncio

async def test_create_user(db_session: AsyncSession):
    email = "test@example.com"
    password = "testpass123"
    user_in = UserCreate(email=email, password=password)
    user = await crud_user.user.create(db_session, obj_in=user_in)
    
    assert user.email == email
    assert hasattr(user, "hashed_password")
    assert verify_password(password, user.hashed_password)

async def test_get_user(db_session: AsyncSession):
    email = "test@example.com"
    password = "testpass123"
    user_in = UserCreate(email=email, password=password)
    user = await crud_user.user.create(db_session, obj_in=user_in)
    
    stored_user = await crud_user.user.get(db_session, id=user.id)
    assert stored_user
    assert user.email == stored_user.email
    assert user.hashed_password == stored_user.hashed_password 