from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from src.auth import authenticate_user, create_access_token, get_password_hash
from src.database import get_db
from src.models import User
from src.schemas.auth import Token, UserSignup
from src.settings import Settings

settings = Settings()
router = APIRouter()


@router.post('/login/', response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(seconds=settings.auth_access_token_expiry_seconds)
    access_token = create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/signup/', response_model=Token)
async def signup_with_email(data: UserSignup, db: Session = Depends(get_db)):
    if User.manager(db).exists(email=data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this email already exists',
        )

    user = User.manager(db).create(
        User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password_hash=get_password_hash(data.password),
        )
    )
    access_token_expires = timedelta(seconds=settings.auth_access_token_expiry_seconds)
    access_token = create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}
