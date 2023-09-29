from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

from app.crud.crud_users import get_user_by_email, get_user_by_username
from app.core.config import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")
crypt_context = CryptContext(schemes=["sha256_crypt"])

async def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)

async def get_password_hash(password):
    return crypt_context.hash(password)

async def authenticate_user_by_username(username: str, password: str, db: AsyncSession):
    db_user = await get_user_by_username(db=db, username=username)
    if not db_user:
        db_user = False
    else:
        if not await verify_password(password, db_user.hashed_password):
            db_user = False
    
    return db_user

async def authenticate_user_by_email(email: str, password: str, db: AsyncSession):
    db_user = await get_user_by_email(db=db, email=email)
    
    if not db_user:
        db_user = False
    else:
        if not await verify_password(password, db_user.hashed_password):
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
