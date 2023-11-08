import time

from fastapi import HTTPException, Request, Depends, status
from redis.asyncio import Redis, ConnectionPool

from app.api.dependencies import get_current_user

pool: ConnectionPool | None = None
client: Redis | None = None
