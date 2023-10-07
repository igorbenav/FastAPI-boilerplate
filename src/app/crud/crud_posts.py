from app.crud.crud_base import CRUDBase
from app.models.post import Post
from app.schemas.post import PostCreateInternal, PostUpdate, PostUpdateInternal, PostDelete

CRUDPost = CRUDBase[Post, PostCreateInternal, PostUpdate, PostUpdateInternal, PostDelete]
crud_posts = CRUDPost(Post)
