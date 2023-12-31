from ..models.post import Post
from ..schemas.post import PostCreateInternal, PostDelete, PostUpdate, PostUpdateInternal
from .crud_base import CRUDBase

CRUDPost = CRUDBase[Post, PostCreateInternal, PostUpdate, PostUpdateInternal, PostDelete]
crud_posts = CRUDPost(Post)
