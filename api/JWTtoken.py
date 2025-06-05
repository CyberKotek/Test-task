import os
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
import schemas


SECRET_KEY = os.environ["SECRET_KEY"] # gen: openssl rand -hex 32
ALGORITHM = os.environ["ALGORITHM"]


def create_access_token(data: dict, expires_delta: int = 15):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
        return token_data
    except InvalidTokenError:
        raise credentials_exception