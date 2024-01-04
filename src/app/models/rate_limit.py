from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class RateLimit(Base):
    __tablename__ = "rate_limit"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
    tier_id: Mapped[int] = mapped_column(ForeignKey("tier.id"), index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    path: Mapped[str] = mapped_column(String, nullable=False)
    limit: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
