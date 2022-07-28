from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from src.database import get_db
from src.models import User
from src.schemas.auth import TokenData
from src.schemas.users import GetUserProfile, UserPasswordHash
from src.settings import Settings

settings = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

HASH_ALGORITHM = 'HS256'


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(db: Session, username: str, password: str):
    user = await get_user_login_details(db, username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    data.update({'exp': datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(data, settings.auth_secret_key, algorithm=HASH_ALGORITHM)
    return encoded_jwt


async def get_user_login_details(db: Session, email: str) -> Optional[UserPasswordHash]:
    user = User.manager(db).filter(email=email).first()
    if user:
        return UserPasswordHash(**user.as_dict())


async def get_user_full(db: Session, email: str) -> Optional[GetUserProfile]:
    user = User.manager(db).get(email=email)
    if user:
        return GetUserProfile(**user.as_dict())


def get_token_data(token, exception=None):
    payload = jwt.decode(token, settings.auth_secret_key, algorithms=[HASH_ALGORITHM])
    email: str = payload.get('sub')
    if exception and email is None:
        raise exception
    return TokenData(email=email)


async def get_user_with_token_data(db, token_data, exception=None):
    user = await get_user_full(db, email=token_data.email)
    if exception and user is None:
        raise exception
    return user


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> GetUserProfile:
    """
    If no user found for the token, then raise a 401
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        token_data = get_token_data(token, exception=credentials_exception)
    except JWTError:
        raise credentials_exception
    else:
        return await get_user_with_token_data(db, token_data, exception=credentials_exception)


async def get_current_user_or_none(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> GetUserProfile:
    token_data = get_token_data(token)
    return await get_user_with_token_data(db, token_data)
