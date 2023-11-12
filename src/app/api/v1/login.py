from typing import Annotated
from datetime import timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import fastapi

from app.core.database import async_get_db
from app.core.models import Token
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, authenticate_user
from app.api.exceptions import credentials_exception

router = fastapi.APIRouter(tags=["login"])

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    
    user = await authenticate_user(
        username_or_email=form_data.username, 
        password=form_data.password, 
        db=db
    )
    if not user:
        raise credentials_exception
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
