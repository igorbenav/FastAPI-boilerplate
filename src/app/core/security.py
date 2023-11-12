from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

from app.crud.crud_users import crud_users
from app.core.config import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")
crypt_context = CryptContext(schemes=["sha256_crypt"])

async def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return crypt_context.hash(password)

async def authenticate_user(username_or_email: str, password: str, db: AsyncSession):
    if "@" in username_or_email:
        db_user = await crud_users.get(db=db, email=username_or_email)
    else: 
        db_user = await crud_users.get(db=db, username=username_or_email)
    
    if (not db_user) or (db_user["is_deleted"]):
        db_user = False
    
    elif not await verify_password(password, db_user["hashed_password"]):
        db_user = False
    
    return db_user

async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
