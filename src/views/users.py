from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.auth import get_current_user
from src.crud import get_object_or_404
from src.database import get_db
from src.exceptions import IntegrityException
from src.models import Board, User
from src.schemas.board import BoardListSchema
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


@router.get('/boards/', response_model=BoardListSchema)
async def get_board(db: Session = Depends(get_db), user: GetUserProfile = Depends(get_current_user)):
    return {'boards': Board.manager(db).filter(user_id=user.id).order_by(Board.created.desc()).all()}


@router.delete('/boards/{board_id}/', status_code=200)
async def delete_board(board_id: int, db: Session = Depends(get_db), user: GetUserProfile = Depends(get_current_user)):
    get_object_or_404(db, Board, id=board_id, user_id=user.id)
    Board.manager(db).delete(id=board_id)
    return
