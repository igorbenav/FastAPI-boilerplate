from typing import Annotated

from app.core.security import SECRET_KEY, ALGORITHM, oauth2_scheme

from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from fastapi import Depends, HTTPException

from app.core.database import async_get_db
from app.core.models import TokenData
from app.models.user import User
from app.crud.crud_users import crud_users
from app.api.exceptions import credentials_exception, privileges_exception

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[AsyncSession, Depends(async_get_db)]) -> User:
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
    
    if user is None:
        raise credentials_exception
    
    if user.is_deleted:
        raise HTTPException(status_code=400, detail="User deleted")

    return user

async def get_current_superuser(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.is_superuser:
        raise privileges_exception
    
    return current_user
