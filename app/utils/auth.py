from datetime import datetime, timedelta, timezone
from datetime import datetime, timedelta
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.constant import JWT_SECRET_KEY, ALGORITHM
from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.schema import Users


async def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def getCurrentUserInfo(dbConn, token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    token = token[7:]
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    userInfo = await getUserInfo(dbConn, emailId=username)
    if userInfo is None:
        raise credentials_exception
    return userInfo

async def getUserInfo(dbConn, emailId):
    userInfo = dbConn.query(Users).filter(Users.emailId == emailId).first()
    return userInfo
