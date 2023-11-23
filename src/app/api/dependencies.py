from typing import Annotated

from app.core.security import SECRET_KEY, ALGORITHM, oauth2_scheme
from app.core.config import settings

from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from fastapi import (
    Depends, 
    HTTPException, 
    Request
)

from app.api.exceptions import credentials_exception, privileges_exception
from app.core.db.database import async_get_db
from app.core.logger import logging
from app.core.schemas import TokenData
from app.core.utils.rate_limit import is_rate_limited
from app.core.security import verify_token
from app.crud.crud_rate_limit import crud_rate_limits
from app.crud.crud_tier import crud_tiers
from app.crud.crud_users import crud_users
from app.models.user import User
from app.schemas.rate_limit import sanitize_path

logger = logging.getLogger(__name__)

DEFAULT_LIMIT = settings.DEFAULT_RATE_LIMIT_LIMIT
DEFAULT_PERIOD = settings.DEFAULT_RATE_LIMIT_PERIOD

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username_or_email: str = payload.get("sub")
        if username_or_email is None:
            raise credentials_exception
        token_data = TokenData(username_or_email=username_or_email)
    
    except JWTError:
        raise credentials_exception
    
    if "@" in username_or_email:
        user = await crud_users.get(db=db, email=token_data.username_or_email)
    else: 
        user = await crud_users.get(db=db, username=token_data.username_or_email)
    
    if user and not user["is_deleted"]:
        return user
    
    raise credentials_exception


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict:
    token_data = await verify_token(token, db)
    if token_data is None:
        raise credentials_exception

    if "@" in token_data.username_or_email:
        user = await crud_users.get(db=db, email=token_data.username_or_email, is_deleted=False)
    else: 
        user = await crud_users.get(db=db, username=token_data.username_or_email, is_deleted=False)
    
    if user:
        return user

    raise credentials_exception


async def get_optional_user(
    request: Request,
    db: AsyncSession = Depends(async_get_db)
) -> dict | None:
    token = request.headers.get("Authorization")
    if not token:
        return None

    try:
        token_type, _, token_value = token.partition(' ')
        if token_type.lower() != 'bearer' or not token_value:
            return None

        token_data = await verify_token(token_value, db)
        if token_data is None:
            return None

        return await get_current_user(token_value, is_deleted=False, db=db)
    
    except HTTPException as http_exc:
        if http_exc.status_code != 401:
            logger.error(f"Unexpected HTTPException in get_optional_user: {http_exc.detail}")
        return None
    
    except Exception as exc:
        logger.error(f"Unexpected error in get_optional_user: {exc}")
        return None


async def get_current_superuser(current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    if not current_user["is_superuser"]:
        raise privileges_exception
    
    return current_user


async def rate_limiter(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    user: User | None = Depends(get_optional_user)
):
    path = sanitize_path(request.url.path)
    if user:
        user_id = user["id"]
        tier = await crud_tiers.get(db, id=user["tier_id"])
        if tier:
            rate_limit = await crud_rate_limits.get(
                db=db,
                tier_id=tier["id"],
                path=path
            )
            if rate_limit:
                limit, period = rate_limit["limit"], rate_limit["period"]
            else:
                logger.warning(f"User {user_id} with tier '{tier['name']}' has no specific rate limit for path '{path}'. Applying default rate limit.")
                limit, period = DEFAULT_LIMIT, DEFAULT_PERIOD
        else:
            logger.warning(f"User {user_id} has no assigned tier. Applying default rate limit.")
            limit, period = DEFAULT_LIMIT, DEFAULT_PERIOD
    else:
        user_id = request.client.host
        limit, period = DEFAULT_LIMIT, DEFAULT_PERIOD

    is_limited = await is_rate_limited(
        db=db,
        user_id=user_id,
        path=path,
        limit=limit,
        period=period
    )
    if is_limited:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )
