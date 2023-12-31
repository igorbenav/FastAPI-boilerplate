from ..models.user import User
from ..schemas.user import UserCreateInternal, UserDelete, UserUpdate, UserUpdateInternal
from .crud_base import CRUDBase

CRUDUser = CRUDBase[User, UserCreateInternal, UserUpdate, UserUpdateInternal, UserDelete]
crud_users = CRUDUser(User)
