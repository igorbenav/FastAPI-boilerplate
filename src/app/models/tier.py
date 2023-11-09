from typing import Optional, List
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class RateLimit(Base):
    __tablename__ = "rate_limit"
    
    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    path: Mapped[str] = mapped_column(String, nullable=False)
    limit: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[int] = mapped_column(Integer, nullable=False)

    tier_rate_limits: Mapped["TierRateLimit"] = relationship(back_populates="rate_limit", cascade="all, delete", lazy="selectin", default_factory=list)


class Tier(Base):
    __tablename__ = "tier"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    users: Mapped[List["User"]] = relationship(back_populates="tier", cascade="save-update, merge", lazy="selectin", default_factory=list)
    tier_rate_limits: Mapped["TierRateLimit"] = relationship(back_populates="tier", cascade="all, delete", lazy="selectin", default_factory=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default_factory=datetime.utcnow
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)


class TierRateLimit(Base):
    __tablename__ = "tier_rate_limit"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False
    )
    
    rate_limit_id: Mapped[int] = mapped_column(ForeignKey("rate_limit.id"), index=True)
    tier_id: Mapped[int] = mapped_column(ForeignKey("tier.id"), index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default_factory=datetime.utcnow
    ) 

    tier: Mapped[Tier] = relationship(back_populates="tier_rate_limits", init=False)
    rate_limit: Mapped[RateLimit] = relationship(back_populates="tier_rate_limits", init=False)
