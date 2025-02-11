from fastcrud import FastCRUD

from ..models.post import Post
from ..schemas.post import PostCreateInternal, PostDelete, PostUpdate, PostUpdateInternal

CRUDPost = FastCRUD[Post, PostCreateInternal, PostUpdate, PostUpdateInternal, PostDelete, None]
crud_posts = CRUDPost(Post)
