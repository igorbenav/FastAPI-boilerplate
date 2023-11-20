from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.core.models import TokenData
from app.crud.crud_token_blacklist import crud_token_blacklist
from app.crud.crud_users import crud_users

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

async def verify_token(token: str, db: AsyncSession) -> TokenData | None:
    """
    Verify a JWT token and return TokenData if valid.

    Parameters
    ----------
    token: str 
        The JWT token to be verified.
    db: AsyncSession 
        Database session for performing database operations.

    Returns
    -------
    TokenData | None
        TokenData instance if the token is valid, None otherwise.
    """
    is_blacklisted = await crud_token_blacklist.exists(db, token=token)
    if is_blacklisted:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username_or_email: str = payload.get("sub")
        if username_or_email is None:
            return None
        return TokenData(username_or_email=username_or_email)
    
    except JWTError:
        return None
