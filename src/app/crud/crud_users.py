from fastcrud import FastCRUD

from ..models.user import User
from ..schemas.user import UserCreateInternal, UserDelete, UserUpdate, UserUpdateInternal

CRUDUser = FastCRUD[User, UserCreateInternal, UserUpdate, UserUpdateInternal, UserDelete]
crud_users = CRUDUser(User)
