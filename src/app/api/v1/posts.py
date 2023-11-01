from typing import List, Annotated

from fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import fastapi

from app.schemas.post import PostCreate, PostUpdate, PostRead, PostCreateInternal
from app.schemas.user import UserRead
from app.api.dependencies import get_current_user, get_current_superuser
from app.core.database import async_get_db
from app.crud.crud_posts import crud_posts
from app.crud.crud_users import crud_users
from app.api.exceptions import privileges_exception
from app.core.cache import cache

router = fastapi.APIRouter(tags=["posts"])

@router.post("/{username}/post", response_model=PostRead, status_code=201)
async def write_post(
    request: Request, 
    username: str,
    post: PostCreate, 
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_user = await crud_users.get(db=db, username=username, is_deleted=False)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if current_user.id != db_user.id:
        raise privileges_exception

    post_internal_dict = post.model_dump()
    post_internal_dict["created_by_user_id"] = db_user.id

    post_internal = PostCreateInternal(**post_internal_dict)
    return await crud_posts.create(db=db, object=post_internal)


@router.get("/{username}/posts", response_model=List[PostRead])
@cache(key_prefix="{username}_posts", resource_id_name="username")
async def read_posts(
    request: Request,
    username: str, 
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_user = await crud_users.get(db=db, username=username, is_deleted=False)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    posts = await crud_posts.get_multi(db=db, created_by_user_id=db_user.id, is_deleted=False)
    return posts


@router.get("/{username}/post/{id}", response_model=PostRead)
@cache(key_prefix="{username}_post_cache", resource_id_name="id")
async def read_post(
    request: Request, 
    username: str,
    id: int, 
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_user = await crud_users.get(db=db, username=username, is_deleted=False)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_post = await crud_posts.get(db=db, id=id, created_by_user_id=db_user.id, is_deleted=False)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return db_post


@router.patch("/{username}/post/{id}")
@cache(
    "{username}_post_cache", 
    resource_id_name="id", 
    to_invalidate_extra={"{username}_posts": "{username}"}
)
async def patch_post(
    request: Request,
    username: str,
    id: int,
    values: PostUpdate,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_user = await crud_users.get(db=db, username=username, is_deleted=False)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if current_user.id != db_user.id:
        raise privileges_exception

    db_post = await crud_posts.get(db=db, id=id, is_deleted=False)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await crud_posts.update(db=db, object=values, id=id)
    return {"message": "Post updated"}


@router.delete("/{username}/post/{id}")
@cache(
    "{username}_post_cache", 
    resource_id_name="id", 
    to_invalidate_extra={"{username}_posts": "{username}"}
)
async def erase_post(
    request: Request, 
    username: str,
    id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_user = await crud_users.get(db=db, username=username, is_deleted=False)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if current_user.id != db_user.id:
        raise privileges_exception

    db_post = await crud_posts.get(db=db, id=id, is_deleted=False)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await crud_posts.delete(db=db, db_row=db_post, id=id)
    
    return {"message": "Post deleted"}


@router.delete("/{username}/db_post/{id}", dependencies=[Depends(get_current_superuser)])
@cache(
    "{username}_post_cache", 
    resource_id_name="id", 
    to_invalidate_extra={"{username}_posts": "{username}"}
)
async def erase_db_post(
    request: Request, 
    username: str,
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_user = await crud_users.get(db=db, username=username, is_deleted=False)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_post = await crud_posts.get(db=db, id=id, is_deleted=False)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await crud_posts.db_delete(db=db, db_object=db_post, id=id)
    return {"message": "Post deleted from the database"}
