from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jwt import PyJWTError
import jwt
from datetime import datetime, timedelta, timezone
from passlib.hash import argon2


import os
from dotenv import load_dotenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes =  60*24 #int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_access_token(data: dict):
    to_encode = data.copy()
    print("inside token")
    expire = datetime.now(timezone.utc) + timedelta(minutes=access_token_expire_minutes)
    print("inside token2")
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = User.from_dict({"username": username})
        return token_data
    except PyJWTError:
        raise credentials_exception

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
