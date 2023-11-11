from typing import Annotated
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.core.models import TimestampModel

class RateLimitBase(BaseModel):
    path: Annotated[
        str, 
        Field(examples=["users"])
    ]
    limit: Annotated[
        int,
        Field(examples=[5])
    ]
    period: Annotated[
        int,
        Field(examples=[60])
    ]


class RateLimit(TimestampModel, RateLimitBase):
    tier_id: int
    name: Annotated[
        str | None,
        Field(
            default=None,
            examples=["users:5:60"]
        )
    ]


class RateLimitRead(RateLimitBase):
    id: int
    tier_id: int
    name: str


class RateLimitCreate(RateLimitBase):
    model_config = ConfigDict(extra='forbid')
    
    name: Annotated[
        str | None,
        Field(
            default=None,
            examples=["api_v1_users:5:60"]
        )
    ]


class RateLimitCreateInternal(RateLimitCreate):
    tier_id: int


class RateLimitUpdate(BaseModel):
    path: str | None = None
    limit: int | None = None
    period: int | None = None
    name: str | None = None


class RateLimitUpdateInternal(RateLimitUpdate):
    updated_at: datetime


class RateLimitDelete(BaseModel):
    pass
