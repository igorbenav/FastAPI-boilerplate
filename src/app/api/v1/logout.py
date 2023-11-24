from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.core.security import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.core.db.database import async_get_db
from app.core.db.crud_token_blacklist import crud_token_blacklist
from app.core.schemas import TokenBlacklistCreate
from app.core.exceptions.http_exceptions import UnauthorizedException

router = APIRouter(tags=["login"])

@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(async_get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expires_at = datetime.fromtimestamp(payload.get("exp"))
        await crud_token_blacklist.create(
            db, 
            object=TokenBlacklistCreate(
                **{"token": token, "expires_at": expires_at}
            )
        )
        return {"message": "Logged out successfully"}
    
    except JWTError:
        raise UnauthorizedException("Invalid token.")
