from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email, username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

privileges_exception = HTTPException(
    status_code=403, 
    detail="The user doesn't have enough privileges"
)
