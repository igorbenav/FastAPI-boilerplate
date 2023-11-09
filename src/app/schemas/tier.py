from typing import Annotated
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.core.models import TimestampModel

# -------------- Rate Limit --------------
class RateLimitBase(BaseModel):
    path: Annotated[
        str, 
        Field(examples=["/users"])
    ]
    limit: Annotated[
        int,
        Field(examples=[5])
    ]
    period: Annotated[
        int,
        Field(example=[60])
    ]
    name: Annotated[
        str | None,
        Field(
            default=None,
            examples=["/users:5:60"]
        )
    ]


class RateLimit(TimestampModel, RateLimitBase):
    pass


class RateLimitRead(RateLimitBase):
    id: int


class RateLimitCreate(RateLimitBase):
    model_config = ConfigDict(extra='forbid')


class RateLimitCreateInternal(RateLimitCreate):
    pass


class RateLimitUpdate(BaseModel):
    pass


class RateLimitDelete(BaseModel):
    pass

# -------------- Tier --------------
class TierBase(BaseModel):
    name: Annotated[
        str, 
        Field(examples=["free"])
    ]


class Tier(TimestampModel, TierBase):
    pass


class TierRead(TierBase):
    id: int
    created_at: datetime


class TierCreate(TierBase):
    pass


class TierCreateInternal(TierCreate):
    pass


class TierUpdate(BaseModel):
    name: str | None = None


class TierUpdateInternal(TierUpdate):
    updated_at: datetime


class TierDelete(BaseModel):
    pass


# -------------- Tier Rate Limit --------------
class TierRateLimitBase(BaseModel):
    rate_limit_id: int
    tier_id: int


class TierRateLimit(TimestampModel, TierRateLimitBase):
    id: int
    created_at: datetime


class TierRateLimitRead(TierRateLimitBase):
    pass


class TierRateLimitCreate(TierRateLimitBase):
    pass


class TierRateLimitCreateInternal(TierRateLimitCreate):
    pass


class TierRateLimitUpdate(BaseModel):
    pass


class TierRateLimitUpdateInternal(TierRateLimitUpdate):
    pass


class TierRateLimitDelete(BaseModel):
    pass
