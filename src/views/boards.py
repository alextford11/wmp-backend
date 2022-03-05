from operator import itemgetter

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Board
from src.schemas import BoardGetSchema

router = APIRouter()


@router.post('/board/create/', response_model=BoardGetSchema)
async def create_board(db: Session = Depends(get_db)):
    board = Board()
    board = Board.manager(db).create(board)
    return board


@router.get('/board/{board_id}/')
async def get_board(board_id: int, db: Session = Depends(get_db)):
    board = db.query(Board).get(board_id)
    board_data = BoardGetSchema(id=board.id, board_workouts=board.board_workouts).dict()
    board_data['board_workout_order'] = [
        workout['id'] for workout in sorted(board_data['board_workouts'], key=itemgetter('sort_value'))
    ]
    return board_data


# {
#     'board': {
#         'workouts': {
#             'workout-1': {
#                 'id': 'workout-1',
#                 'name': 'Push Up',
#                 'muscles': {
#                     'muscle-2': {
#                         'id': 'muscle-2',
#                         'name': 'Chest',
#                     },
#                     'muscle-3': {
#                         'id': 'muscle-3',
#                         'name': 'Biceps',
#                     },
#                 },
#             },
#             'workout-2': {
#                 'id': 'workout-2',
#                 'name': 'High Cable Fly',
#                 'muscles': {
#                     'muscle-1': {
#                         'id': 'muscle-1',
#                         'name': 'Shoulders',
#                     },
#                     'muscle-2': {
#                         'id': 'muscle-2',
#                         'name': 'Chest',
#                     },
#                     'muscle-3': {
#                         'id': 'muscle-3',
#                         'name': 'Triceps',
#                     },
#                 },
#             },
#         },
#         'workout_order': ['workout-1', 'workout-2'],
#     }
# }
