from typing import TypeVar, Generic, List
import uuid as uuid_pkg
from datetime import datetime

from pydantic import BaseModel, Field, field_serializer
from sqlalchemy import text

ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)

class ListResponse(BaseModel, Generic[ReadSchemaType]):
    data: List[ReadSchemaType]


class PaginatedListResponse(ListResponse[ReadSchemaType]):
    total_count: int
    has_more: bool
    page: int | None = None
    items_per_page: int | None = None


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

    @field_serializer("created_at")
    def serialize_dt(self, created_at: datetime | None, _info):
        return created_at.isoformat()

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime | None, _info):
        if updated_at is not None:
            return updated_at.isoformat()


class PersistentDeletion(BaseModel):
    deleted_at: datetime | None = Field(
        default=None,
        json_schema_extra={
            "server_default": text("None"),
            "ondelete": text("current_timestamp(0)")
        }
    )

    is_deleted: bool = False

    @field_serializer('deleted_at')
    def serialize_dates(self, deleted_at: datetime | None, _info):
        if deleted_at is not None:
            return deleted_at.isoformat()
