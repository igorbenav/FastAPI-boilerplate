from datetime import datetime
from typing import Union, Dict

from fastapi import HTTPException, Request, Depends, status
from redis.asyncio import Redis, ConnectionPool
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logging
from app.schemas.user import UserRead
from app.schemas.tier import TierRead
from app.crud.crud_users import crud_users


logger = logging.getLogger(__name__)

pool: ConnectionPool | None = None
client: Redis | None = None
