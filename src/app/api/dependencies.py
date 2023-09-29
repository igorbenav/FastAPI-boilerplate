from typing import Annotated

from app.core.security import SECRET_KEY, ALGORITHM, oauth2_scheme

from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status

from app.core.database import async_get_db
from app.crud.crud_users import get_user_by_email, get_user_by_username
from app.core.models import TokenData

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[AsyncSession, Depends(async_get_db)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username_or_email: str = payload.get("sub")
        if username_or_email is None:
            raise credentials_exception
        token_data = TokenData(username_or_email=username_or_email)
    
    except JWTError:
        raise credentials_exception
    
    if "@" in username_or_email:
        user = await get_user_by_email(db=db, email=token_data.username_or_email)
    else: 
        user = await get_user_by_username(db=db, username=token_data.username_or_email)
    
    if user is None:
        raise credentials_exception
    
    if user.is_deleted:
        raise HTTPException(status_code=400, detai="User deleted")

    return user
