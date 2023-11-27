from typing import Dict

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.core.security import oauth2_scheme, blacklist_token
from app.core.db.database import async_get_db
from app.core.exceptions.http_exceptions import UnauthorizedException

router = APIRouter(tags=["login"])

@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(async_get_db)
) -> Dict[str, str]:
    try:
        await blacklist_token(token=token, db=db)
        return {"message": "Logged out successfully"}
    
    except JWTError:
        raise UnauthorizedException("Invalid token.")
