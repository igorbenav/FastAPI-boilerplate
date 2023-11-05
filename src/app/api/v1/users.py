from typing import List, Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
import fastapi

from app.schemas.user import UserCreate, UserCreateInternal, UserUpdate, UserRead 
from app.api.dependencies import get_current_user, get_current_superuser
from app.core.database import async_get_db
from app.core.security import get_password_hash
from app.crud.crud_users import crud_users
from app.api.exceptions import privileges_exception
from app.api.paginated import PaginatedListResponse, paginated_response, compute_offset

router = fastapi.APIRouter(tags=["users"])

@router.post("/user", response_model=UserRead, status_code=201)
async def write_user(
    request: Request, 
    user: UserCreate, 
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    email_row = await crud_users.exists(db=db, email=user.email)
    if email_row:
        raise HTTPException(status_code=400, detail="Email is already registered")

    username_row = await crud_users.exists(db=db, username=user.username)
    if username_row:
        raise HTTPException(status_code=400, detail="Username not available")
    
    user_internal_dict = user.model_dump()
    user_internal_dict["hashed_password"] = get_password_hash(password=user_internal_dict["password"])
    del user_internal_dict["password"]

    user_internal = UserCreateInternal(**user_internal_dict)
    return await crud_users.create(db=db, object=user_internal)


@router.get("/users", response_model=PaginatedListResponse[UserRead])
async def read_users(
    request: Request, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10
):
    users_data = await crud_users.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=UserRead, 
        is_deleted=False
    )
    
    return paginated_response(
        crud_data=users_data, 
        page=page, 
        items_per_page=items_per_page
    )


@router.get("/user/me/", response_model=UserRead)
async def read_users_me(
    request: Request, current_user: Annotated[UserRead, Depends(get_current_user)]
):
    return current_user


@router.get("/user/{username}", response_model=UserRead)
async def read_user(request: Request, username: str, db: Annotated[AsyncSession, Depends(async_get_db)]):
    db_user = await crud_users.get(db=db, schema_to_select=UserRead, username=username, is_deleted=False)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@router.patch("/user/{username}")
async def patch_user(
    request: Request, 
    values: UserUpdate,
    username: str,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_user = await crud_users.get(db=db, schema_to_select=UserRead, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user.username != current_user.username:
        raise privileges_exception
    
    if values.username != db_user.username:
        existing_username = await crud_users.exists(db=db, username=values.username)
        if existing_username:
            raise HTTPException(status_code=400, detail="Username not available")

    if values.email != db_user.email:
        existing_email = await crud_users.exists(db=db, email=values.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email is already registered")

    await crud_users.update(db=db, object=values, username=username)
    return {"message": "User updated"}


@router.delete("/user/{username}")
async def erase_user(
    request: Request, 
    username: str, 
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_user = await crud_users.get(db=db, schema_to_select=UserRead, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if username != current_user.username:
        raise privileges_exception

    await crud_users.delete(db=db, db_row=db_user, username=username)
    return {"message": "User deleted"}


@router.delete("/db_user/{username}", dependencies=[Depends(get_current_superuser)])
async def erase_db_user(
    request: Request, 
    username: str,
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_user = await crud_users.exists(db=db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user = await crud_users.db_delete(db=db, username=username)
    return {"message": "User deleted from the database"}
