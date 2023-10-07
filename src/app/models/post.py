from typing import Optional
import uuid as uuid_pkg
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False
    )
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    title: Mapped[str] = mapped_column(String(30))
    text: Mapped[str] = mapped_column(String(63206))
    media_url: Mapped[str | None] = mapped_column(String, default=None)

    user: Mapped["User"] = relationship(back_populates="posts", lazy="selectin", init=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default_factory=datetime.utcnow
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False)
