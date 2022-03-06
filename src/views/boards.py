from operator import itemgetter

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Board
from src.schemas import BoardGetSchema, UpdateWorkoutOrderSchema

router = APIRouter(prefix='/board')


@router.post('/create/', response_model=BoardGetSchema)
async def create_board(db: Session = Depends(get_db)):
    board = Board()
    board = Board.manager(db).create(board)
    return board


@router.get('/{board_id}/')
async def get_board(board_id: int, db: Session = Depends(get_db)):
    board = db.query(Board).get(board_id)
    board_data = BoardGetSchema(id=board.id, board_workouts=board.board_workouts).dict()
    board_data['board_workout_order'] = [
        workout['id'] for workout in sorted(board_data['board_workouts'], key=itemgetter('sort_value'))
    ]
    return board_data


@router.post('/{board_id}/update_order/')
async def update_board_workout_order(board_id: int, data: UpdateWorkoutOrderSchema, db: Session = Depends(get_db)):
    board = db.query(Board).get(board_id)
    if len(board.board_workouts) != len(set(data.workout_order)):
        raise HTTPException(status_code=400, detail='New order contains less workouts than saved workouts')

    new_sort_value_lu = {bw_id: index + 1 for index, bw_id in enumerate(data.workout_order)}
    for board_workout in board.board_workouts:
        try:
            board_workout.sort_value = new_sort_value_lu[board_workout.id]
            db.add(board_workout)
        except KeyError:
            raise HTTPException(status_code=400, detail='New order contains values which are not linked to this board')
    db.commit()
    return HTTPException(status_code=200)
