import uuid as uuid_pkg
from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean, text

class UUIDMixin:
    uuid: uuid_pkg.UUID = Column(uuid_pkg.UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4, server_default=text("gen_random_uuid()"))

class TimestampMixin:
    created_at: datetime = Column(DateTime, default=datetime.utcnow, server_default=text("current_timestamp(0)"))
    updated_at: datetime = Column(DateTime, nullable=True, onupdate=datetime.utcnow, server_default=text("current_timestamp(0)"))

class SoftDeleteMixin:
    deleted_at: datetime = Column(DateTime, nullable=True)
    is_deleted: bool = Column(Boolean, default=False)
