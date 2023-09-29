from typing import Annotated
from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import fastapi
from app.core.database import async_get_db
from app.core.models import Token
from app.core.security import create_access_token, authenticate_user_by_username, authenticate_user_by_email, ACCESS_TOKEN_EXPIRE_MINUTES

router = fastapi.APIRouter(tags=["login"])

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(async_get_db)
):
    if "@" in form_data.username:
        user = await authenticate_user_by_email(form_data.username, form_data.password, db=db)
    else:
        user = await authenticate_user_by_username(form_data.username, form_data.password, db=db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email, username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
