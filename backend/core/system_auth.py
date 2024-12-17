from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
import jwt

from core.config import settings


def hash_password(pwd: str) -> str:
    """使用 bcrypt 对密码进行加密"""

    pwd_bytes = pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    pwd_hashed = bcrypt.hashpw(pwd_bytes, salt)
    return pwd_hashed.decode('utf-8')


def verify_password(pwd: str, pwd_hashed: str) -> bool:
    return bcrypt.checkpw(pwd.encode("utf-8"), pwd_hashed.encode("utf-8"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
