from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampedBase

class URL(TimestampedBase):
    """URL model for storing url related data"""
    __tablename__ = "urls"  # Explicit table name
    
    original_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    visits: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_visit: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="urls")