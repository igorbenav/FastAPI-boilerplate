from typing import List, Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import fastapi

from app.schemas.user import UserCreate, UserUpdate, UserRead, UserBase
from app.api.dependencies import get_current_user, get_current_superuser
from app.core.database import async_get_db
from ...crud.crud_users import (
    get_user, 
    get_user_by_email, 
    get_users, 
    create_user, 
    get_user_by_username, 
    update_user,
    delete_user
)
from app.api.dependencies import get_current_user

router = fastapi.APIRouter(tags=["users"])

@router.post("/user", response_model=UserBase, status_code=201)
async def write_user(user: UserCreate, db: AsyncSession = Depends(async_get_db)):
    db_user = await get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    db_user = await get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username not available")

    return await create_user(db=db, user=user)


@router.get("/user", response_model=List[UserRead])
async def read_users(db: AsyncSession = Depends(async_get_db)):
    users = await get_users(db=db)
    return users


@router.get("/user/me/", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[UserRead, Depends(get_current_user)]
):
    return current_user


@router.get("/user/{id}", response_model=UserRead)
async def read_user(id: int, db: AsyncSession = Depends(async_get_db)):
    db_user = await get_user(db=db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user


@router.patch("/users/{id}", response_model=UserUpdate)
async def patch_user(
    values: UserUpdate, 
    id: int, 
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: AsyncSession = Depends(async_get_db)
):
    db_user = await get_user(db=db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't own this user.")
    
    if values.username != db_user.username:
        existing_username = await get_user_by_username(db=db, username=values.username)
        if existing_username is not None:
            raise HTTPException(status_code=400, detail="Username not available")

    if values.email != db_user.email:
        existing_email = await get_user_by_email(db=db, email=values.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email is already registered")

    db_user = await update_user(db=db, id=id, values=values, user=db_user)
    return db_user


@router.delete("/user/{id}")
async def erase_user(
    id: int, 
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: AsyncSession = Depends(async_get_db)
):
    db_user = await get_user(db=db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't own this user.")

    db_user = await delete_user(db=db, id=id, user=db_user)
    return db_user


@router.delete("/db_user/{id}")
async def erase_db_user(
    id: int, 
    current_superuser: Annotated[UserRead, Depends(get_current_superuser)],
    db: AsyncSession = Depends(async_get_db)
):
    db_user = await get_user(db=db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user = await delete_user(db=db, id=id, user=db_user)
    return db_user
