from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID

import bcrypt
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from dotenv import dotenv_values
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError as JWTError
from pydantic import BaseModel

from core.models import User

CONFIG = dotenv_values(".env")

SECRET_KEY = CONFIG.get("SECRET_KEY")

ALGORITHM = CONFIG.get("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(CONFIG.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

RSA_PRIVATE_KEY = CONFIG.get("RSA_PRIVATE_KEY")

RSA_PUBLIC_KEY = CONFIG.get("RSA_PUBLIC_KEY")


class UserModel(BaseModel):
    unique_id: UUID
    name: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def load_rsa_private_key_from_pem():
    with open("./private_key.pem", "rb") as pem_file:
        pem_data = pem_file.read()

    private_key = serialization.load_pem_private_key(
        pem_data,
        password=None,
        backend=default_backend(),
    ).private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return private_key


private_key = load_rsa_private_key_from_pem()


def get_password_hash(password: str):
    return bcrypt.hashpw(
        password.encode("utf-8"), salt=bcrypt.gensalt(prefix=b"2a")
    ).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


async def get_user(username: str):
    user = await User.filter(name=username).first()
    if user:
        return UserModel(username=user.name, email=user.email, unique_id=user.unique_id)


async def authenticate_user(username: str, password: str):
    user = await User.filter(name=username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def login_for_access_token(username: str, password: str) -> Token | None:
    user = await authenticate_user(username, password)
    if not user:
        return None

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"name": user.name, "id": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="JWT")
