from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.url import URL
from app.schemas.url import URLCreate, URLUpdate

class CRUDURL(CRUDBase[URL, URLCreate, URLUpdate]):
    async def get_by_slug(self, db: AsyncSession, *, slug: str) -> Optional[URL]:
        stmt = select(URL).where(URL.slug == slug)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_urls(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[URL]:
        stmt = select(URL).where(URL.user_id == user_id).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def increment_visits(self, db: AsyncSession, *, url: URL) -> URL:
        url.visits += 1
        db.add(url)
        await db.commit()
        await db.refresh(url)
        return url

url = CRUDURL(URL) 