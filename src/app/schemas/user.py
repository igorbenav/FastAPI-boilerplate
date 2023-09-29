from typing import Annotated
from datetime import datetime

from pydantic import BaseModel, EmailStr, StringConstraints, Field, HttpUrl

from app.core.models import UUIDModel, TimestampModel, PersistentDeletion

class UserBase(BaseModel):
    name: Annotated[
        str, 
        Field(
            min_length=2, max_length=30, examples=["User Userson"]
        )
    ]
    username: Annotated[
        str, 
        Field(
            min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userson"]
        )
    ]
    email: Annotated[
        EmailStr, 
        Field(
            examples=["user.userson@example.com"]
        )
    ]


class User(TimestampModel, UserBase, UUIDModel, PersistentDeletion):
    profile_image_url: Annotated[HttpUrl, Field(default="profileimageurl.com")]
    hashed_password: str


class UserRead(BaseModel):
    name: Annotated[
        str, 
        Field(
            min_length=2, max_length=30, examples=["User Userson"]
        )
    ]
    username: Annotated[
        str, 
        Field(
            min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userson"]
        )
    ]
    profile_image_url: Annotated[HttpUrl | None, Field()]


class UserCreate(UserBase):
    password: Annotated[
        str, 
        Field(
            pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$", examples=["Str1ngst!"]
        )
    ]


class UserUpdate(BaseModel):
    name: Annotated[
        str, 
        Field(
            min_length=2, max_length=30, examples=["User Userson"], default=None
        )
    ]
    username: Annotated[
        str, 
        Field(
            min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userson"], default=None
        )
    ]
    email: Annotated[
        EmailStr, 
        Field(
            examples=["user.userson@example.com"], default=None
        )
    ]
    profile_image_url: Annotated[HttpUrl | None, Field(default=None)]


class UserUpdateInternal(UserUpdate):
    updated_at: datetime


class UserDelete(BaseModel):
    is_deleted: bool
    deleted_at: datetime


class UserRestoreDeleted(BaseModel):
    is_deleted: bool
