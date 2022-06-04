from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.auth import get_current_user
from src.database import get_db
from src.exceptions import IntegrityException
from src.models import User
from src.schemas.users import GetUserProfile, UpdateUserProfile

router = APIRouter(prefix='/user')


@router.get('/profile/', response_model=GetUserProfile)
async def user_details(user: GetUserProfile = Depends(get_current_user)):
    return user


@router.put('/profile/')
async def update_user(
    user_data: UpdateUserProfile,
    db: Session = Depends(get_db),
    user: GetUserProfile = Depends(get_current_user),
):
    if cleaned_data := user_data.dict(exclude_none=True):
        for field, value in cleaned_data:
            setattr(user, field, value)
        try:
            User.manager(db).update(user)
        except IntegrityError:
            raise IntegrityException(detail='User with this email already exists')
    return {'detail': 'Profile updated successfully'}
