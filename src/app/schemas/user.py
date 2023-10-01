from typing import Annotated, Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, HttpUrl, ConfigDict

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
    profile_image_url: Annotated[
        str, 
        Field(default="https://www.profileimageurl.com")
    ]
    hashed_password: str
    is_superuser: bool = False


class UserRead(BaseModel):
    id: int
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
    profile_image_url: str


class UserCreate(UserBase):
    model_config = ConfigDict(extra='forbid')

    password: Annotated[
        str, 
        Field(
            pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$", examples=["Str1ngst!"]
        )
    ]


class UserCreateInternal(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: Annotated[
        Optional[str], 
        Field(
            min_length=2, 
            max_length=30, 
            examples=["User Userberg"],
            default=None
        )
    ]
    username: Annotated[
        Optional[str], 
        Field(
            min_length=2, 
            max_length=20, 
            pattern=r"^[a-z0-9]+$", 
            examples=["userberg"],
            default=None
        )
    ]
    email: Annotated[
        Optional[EmailStr],
        Field(
            examples=["user.userberg@example.com"],
            default=None
        )
    ]
    profile_image_url: Annotated[
        Optional[str],
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$",
            examples=["https://www.profileimageurl.com"],
            default=None
        )
    ]


class UserUpdateInternal(UserUpdate):
    updated_at: datetime


class UserDelete(BaseModel):
    model_config = ConfigDict(extra='forbid')

    is_deleted: bool
    deleted_at: datetime


class UserRestoreDeleted(BaseModel):
    is_deleted: bool
