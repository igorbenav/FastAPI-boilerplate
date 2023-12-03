from .crud_base import CRUDBase
from ..models.post import Post
from ..schemas.post import PostCreateInternal, PostUpdate, PostUpdateInternal, PostDelete

CRUDPost = CRUDBase[Post, PostCreateInternal, PostUpdate, PostUpdateInternal, PostDelete]
crud_posts = CRUDPost(Post)
