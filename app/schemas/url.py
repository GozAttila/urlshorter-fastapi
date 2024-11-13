from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl

class URLBase(BaseModel):
    original_url: HttpUrl
    slug: Optional[str] = None

class URLCreate(URLBase):
    pass

class URLUpdate(URLBase):
    pass

class URLInDBBase(URLBase):
    id: int
    visits: int = 0
    last_visit: Optional[datetime] = None
    user_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class URL(URLInDBBase):
    pass

class URLInDB(URLInDBBase):
    pass 