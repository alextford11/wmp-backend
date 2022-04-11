from operator import itemgetter

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud import get_object_or_404
from src.database import get_db
from src.models import Board, BoardWorkout, Workout, Muscle
from src.schemas import BoardGetSchema, UpdateWorkoutOrderSchema, AddWorkoutSchema, RemoveWorkoutSchema

router = APIRouter(prefix='/board')


@router.post('/create/', response_model=BoardGetSchema)
async def create_board(db: Session = Depends(get_db)):
    board = Board()
    board = Board.manager(db).create(board)
    return board


@router.get('/{board_id}/', response_model=BoardGetSchema)
async def get_board(board_id: int, db: Session = Depends(get_db)):
    board = get_object_or_404(db, Board, id=board_id)
    board_data = BoardGetSchema(id=board.id, board_workouts=board.board_workouts).dict()
    board_data['board_workout_order'] = [
        workout['id'] for workout in sorted(board_data['board_workouts'], key=itemgetter('sort_value'))
    ]

    muscles = Muscle.manager(db).all()
    board_muscle_counts = dict(sorted({muscle.name: 0 for muscle in muscles}.items()))
    for board_workout in board.board_workouts:
        workout = board_workout.workout
        for muscle in workout.related_muscles:
            board_muscle_counts[muscle.name] += 1
    board_data['board_muscle_counts'] = dict(sorted(board_muscle_counts.items(), key=itemgetter(1), reverse=True))
    return board_data


@router.post('/{board_id}/update_order/')
async def update_board_workout_order(board_id: int, data: UpdateWorkoutOrderSchema, db: Session = Depends(get_db)):
    board = get_object_or_404(db, Board, id=board_id)
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


@router.post('/{board_id}/add_workout/')
async def add_workout_to_board(board_id: int, data: AddWorkoutSchema, db: Session = Depends(get_db)):
    get_object_or_404(db, Board, id=board_id)
    get_object_or_404(db, Workout, id=data.workout_id)
    BoardWorkout.manager(db).create(BoardWorkout(board_id=board_id, workout_id=data.workout_id))
    return HTTPException(status_code=200)


@router.post('/{board_id}/remove_workout/')
async def remove_workout_from_board(board_id: int, data: RemoveWorkoutSchema, db: Session = Depends(get_db)):
    get_object_or_404(db, Board, id=board_id)
    get_object_or_404(db, Workout, id=data.board_workout_id)
    BoardWorkout.manager(db).delete(id=data.board_workout_id, board_id=board_id)
    return HTTPException(status_code=200)
