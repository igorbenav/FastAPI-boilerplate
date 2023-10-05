from typing import List, Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import fastapi

from app.schemas.user import UserCreate, UserCreateInternal, UserUpdate, UserRead, UserBase 
from app.api.dependencies import get_current_user, get_current_superuser
from app.core.database import async_get_db
from app.core.security import get_password_hash
from app.crud.crud_users import crud_users
from app.api.exceptions import privileges_exception

router = fastapi.APIRouter(tags=["users"])

@router.post("/user", response_model=UserBase, status_code=201)
async def write_user(user: UserCreate, db: AsyncSession = Depends(async_get_db)):
    db_user = await crud_users.get(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    db_user = await crud_users.get(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username not available")
    
    user_internal_dict = user.model_dump()
    user_internal_dict["hashed_password"] = get_password_hash(password=user_internal_dict["password"])
    del user_internal_dict["password"]

    user_internal = UserCreateInternal(**user_internal_dict)
    return await crud_users.create(db=db, object=user_internal)


@router.get("/users", response_model=List[UserRead])
async def read_users(db: AsyncSession = Depends(async_get_db)):
    users = await crud_users.get_multi(db=db, is_deleted=False)
    return users


@router.get("/user/me/", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[UserRead, Depends(get_current_user)]
):
    return current_user


@router.get("/user/{username}", response_model=UserRead)
async def read_user(username: str, db: AsyncSession = Depends(async_get_db)):
    db_user = await crud_users.get(db=db, username=username, is_deleted=False)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user


@router.patch("/user/{username}", response_model=UserUpdate)
async def patch_user(
    values: UserUpdate,
    username: str,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: AsyncSession = Depends(async_get_db)
):
    db_user = await crud_users.get(db=db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user.username != current_user.username:
        raise privileges_exception
    
    if values.username != db_user.username:
        existing_username = await crud_users.get(db=db, username=values.username)
        if existing_username is not None:
            raise HTTPException(status_code=400, detail="Username not available")

    if values.email != db_user.email:
        existing_email = await crud_users.get(db=db, email=values.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email is already registered")

    db_user = await crud_users.update(db=db, object=values, db_object=db_user)
    return db_user


@router.delete("/user/{username}")
async def erase_user(
    username: str, 
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: AsyncSession = Depends(async_get_db)
):
    db_user = await crud_users.get(db=db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user.username != current_user.username:
        raise privileges_exception

    db_user = await crud_users.delete(db=db, db_object=db_user, username=username)
    return db_user


@router.delete("/db_user/{username}")
async def erase_db_user(
    username: str,
    current_superuser: Annotated[UserRead, Depends(get_current_superuser)],
    db: AsyncSession = Depends(async_get_db)
):
    db_user = await crud_users.get(db=db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user = await crud_users.db_delete(db=db, db_object=db_user, username=username)
    return db_user
