from app.crud.crud_base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreateInternal, UserUpdate, UserUpdateInternal, UserDelete

CRUDUser = CRUDBase[User, UserCreateInternal, UserUpdate, UserUpdateInternal, UserDelete]
crud_users = CRUDUser(User)
