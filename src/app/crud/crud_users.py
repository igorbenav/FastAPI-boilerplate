from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from passlib.context import CryptContext
from sqlalchemy import and_

from app.schemas.user import (
    UserCreate, 
    UserUpdate, 
    UserUpdateInternal, 
    UserDelete
)
from app.models.user import User

crypt_context = CryptContext(schemes=["sha256_crypt"])

async def create_user(db: AsyncSession, user: UserCreate):
    user = User(
        username=user.username,
        email=user.email, 
        name=user.name,
        hashed_password=crypt_context.hash(user.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user(db: AsyncSession, id: int):
    query = select(User).where(
        and_(User.id == id, User.is_deleted == False)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(
        and_(User.username == username, User.is_deleted == False)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).where(
        and_(User.email == email, User.is_deleted == False)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession):
    query = select(User).where(User.is_deleted == False)
    result = await db.execute(query)
    return result.scalars().all()

async def update_user(
        db: AsyncSession, 
        id: int, 
        values: UserUpdate, 
        user: User | None = None
):
    user = user or await get_user(db=db, id=id)
    if user is not None:
        internal_values = UserUpdateInternal(
            name=values.name,
            username=values.username,
            email=values.email,
            profile_image_url=values.profile_image_url,
            updated_at=datetime.utcnow()
        )
        query = update(User).where(User.id == id).values(internal_values.dict(exclude_unset=True))
        await db.execute(query)
        await db.commit()
        await db.refresh(user)

    return user

async def delete_user(
        db: AsyncSession, 
        id: int, 
        user: User | None = None
):
    user = user or await get_user(db=db, id=id)
    if user is not None:
        values = UserDelete(
            is_deleted=True,
            deleted_at=datetime.utcnow()
        )
        query = update(User).where(User.id == id).values(values.dict(exclude_unset=True))
        await db.execute(query)
        await db.commit()
        await db.refresh(user)
    
    return user

async def delete_db_user(
        db: AsyncSession, 
        id: int,
        user: User | None = None
):
    user = user or await get_user(db=db, id=id)
    if user is not None:
        query = delete(User).where(User.id == id)
        await db.execute(query)
        await db.commit()

    return user
