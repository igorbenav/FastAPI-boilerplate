from typing import Annotated
from datetime import datetime

from pydantic import BaseModel, Field

from app.core.models import TimestampModel

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
