import uuid as uuid_pkg
from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import text

from app.core.database import Base

class HealthCheck(BaseModel):
    name: str
    version: str
    description: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username_or_email: str | None = None


class UUIDModel(BaseModel):
    uuid: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        json_schema_extra={
            "server_default": text("gen_random_uuid()"),
            "unique": True
        }
    )


class TimestampModel(BaseModel):
    created_at: datetime = Field(
       default_factory=datetime.utcnow,
       json_schema_extra={
           "server_default": text("current_timestamp(0)")
       }
    )

    updated_at: datetime = Field(
       default=None,
       json_schema_extra={
           "server_default": text("current_timestamp(0)"),
           "onupdate": text("current_timestamp(0)")
       }
    )

    
class PersistentDeletion(BaseModel):
    deleted_at: datetime | None = Field(
        default=None,
        json_schema_extra={
            "server_default": text("None"),
            "ondelete": text("current_timestamp(0)")
        }
    )

    is_deleted: bool = False
