from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from src.auth import authenticate_user, create_access_token
from src.database import get_db
from src.schemas.auth import Token
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
