from typing import Annotated, Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.core.models import UUIDModel, TimestampModel, PersistentDeletion

class PostBase(BaseModel):
    title: Annotated[
        str,
        Field(min_length=2, max_length=30, examples=["This is my post"])
    ]
    text: Annotated[
        str, 
        Field(min_length=1, max_length=63206, examples=["This is the content of my post."])
    ]
    

class Post(TimestampModel, PostBase, UUIDModel, PersistentDeletion):
    media_url: Annotated[
        str | None, 
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$",
            examples=["https://www.postimageurl.com"],
            default=None
        ),
    ]
    created_by_user_id: int


class PostRead(BaseModel):
    id: int
    title: Annotated[
        str,
        Field(min_length=2, max_length=30, examples=["This is my post"])
    ]
    text: Annotated[
        str, 
        Field(min_length=1, max_length=63206, examples=["This is the content of my post."])
    ]
    media_url: Annotated[
        str | None, 
        Field(
            examples=["https://www.postimageurl.com"],
            default=None
        ),
    ]
    created_by_user_id: int
    created_at: datetime


class PostCreate(PostBase):
    model_config = ConfigDict(extra='forbid')
    
    media_url: Annotated[
        str | None, 
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$",
            examples=["https://www.postimageurl.com"],
            default=None
        ),
    ]


class PostCreateInternal(PostCreate):
    created_by_user_id: int


class PostUpdate(PostBase):
    model_config = ConfigDict(extra='forbid')
    
    title: Annotated[
        str | None,
        Field(
            min_length=2, 
            max_length=30, 
            examples=["This is my updated post"],
            default=None
        )
    ]
    text: Annotated[
        str | None,
        Field(
            min_length=1, 
            max_length=63206, 
            examples=["This is the updated content of my post."],
            default=None
        )
    ]
    media_url: Annotated[
        str | None,
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$",
            examples=["https://www.postimageurl.com"],
            default=None
        )
    ]


class PostUpdateInternal(PostUpdate):
    updated_at: datetime


class PostDelete(BaseModel):
    model_config = ConfigDict(extra='forbid')

    is_deleted: bool
    deleted_at: datetime
