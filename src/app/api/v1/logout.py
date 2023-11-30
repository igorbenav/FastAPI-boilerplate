from typing import Dict

from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.core.security import oauth2_scheme, blacklist_token
from app.core.db.database import async_get_db
from app.core.exceptions.http_exceptions import UnauthorizedException

router = APIRouter(tags=["login"])

@router.post("/logout")
async def logout(
    response: Response,
    access_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(async_get_db)
) -> Dict[str, str]:
    try:
        await blacklist_token(token=access_token, db=db)
        response.delete_cookie(key="refresh_token")

        return {"message": "Logged out successfully"}
    
    except JWTError:
        raise UnauthorizedException("Invalid token.")
