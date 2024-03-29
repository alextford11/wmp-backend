from operator import itemgetter

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.auth import get_token_data, get_user_with_token_data
from src.crud import get_object_or_404
from src.database import get_db
from src.models import Board, BoardWorkout, BoardWorkoutRecord, Muscle, Workout
from src.schemas.board import BoardGetSchema, CreateBoardSchema, UpdateBoardNameSchema
from src.schemas.forms import SelectGroupInputListSchema, SelectInputListSchema
from src.schemas.utils import MeasurementUnits
from src.schemas.workouts import AddWorkoutSchema, UpdateWorkoutOrderSchema, UpdateWorkoutSchema

router = APIRouter(prefix='/board')


@router.post('/create/', response_model=BoardGetSchema)
async def create_board(data: CreateBoardSchema, db: Session = Depends(get_db)):
    board_data = {}
    if data.user_access_token:
        token_data = get_token_data(data.user_access_token)
        user = await get_user_with_token_data(db, token_data)
        board_data = {'user_id': user.id}
    board = Board(**board_data)
    board = Board.manager(db).create(board)
    return board


@router.get('/{board_id}/', response_model=BoardGetSchema)
async def get_board(board_id: int, db: Session = Depends(get_db)):
    board = get_object_or_404(db, Board, id=board_id)
    board_data = BoardGetSchema(
        id=board.id, name=board.name, created=board.created, board_workouts=board.board_workouts
    ).dict()
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


@router.post('/{board_id}/workout/')
async def add_workout_to_board(board_id: int, data: AddWorkoutSchema, db: Session = Depends(get_db)):
    get_object_or_404(db, Board, id=board_id)
    get_object_or_404(db, Workout, id=data.workout_id)
    BoardWorkout.manager(db).create(BoardWorkout(board_id=board_id, workout_id=data.workout_id))
    return HTTPException(status_code=200)


@router.delete('/{board_id}/workout/{board_workout_id}/')
async def remove_workout_from_board(board_id: int, board_workout_id: int, db: Session = Depends(get_db)):
    get_object_or_404(db, Board, id=board_id)
    get_object_or_404(db, Workout, id=board_workout_id)
    BoardWorkout.manager(db).delete(id=board_workout_id, board_id=board_id)
    return HTTPException(status_code=200)


@router.put('/{board_id}/workout/{board_workout_id}/')
async def update_board_workout(
    board_id: int, board_workout_id: int, data: UpdateWorkoutSchema, db: Session = Depends(get_db)
):
    get_object_or_404(db, Board, id=board_id)
    board_workout: BoardWorkout = get_object_or_404(db, BoardWorkout, id=board_workout_id)

    record_fields = ['sets_value', 'reps_value', 'measurement_value', 'measurement_unit']
    values_updated = False
    for field, value in data.dict().items():
        if value is not None:
            if getattr(board_workout, field) != value:
                setattr(board_workout, field, value)
                if field in record_fields:
                    values_updated = True
    BoardWorkout.manager(db).update(board_workout)
    if values_updated or not BoardWorkoutRecord.manager(db).exists(board_workout_id=board_workout.id):
        # create record when at least one field has been changed or no record exists yet
        bwr = BoardWorkoutRecord(
            board_workout_id=board_workout.id, **{f: getattr(board_workout, f) for f in record_fields}
        )
        BoardWorkoutRecord.manager(db).create(bwr)
    return HTTPException(status_code=200)


@router.get('/measurement-units/list/', response_model=SelectInputListSchema)
async def get_measurement_units_list():
    return {'options': [{'label': unit.label, 'value': unit.value} for unit in list(MeasurementUnits)]}


@router.get('/measurement-units/categories/', response_model=SelectGroupInputListSchema)
async def get_categorised_measurement_units_list():
    return {
        'options': [
            {'label': group, 'options': [{'label': unit.label, 'value': unit.value} for unit in units]}
            for group, units in MeasurementUnits.get_categories().items()
        ]
    }


@router.post('/{board_id}/name/', response_model=BoardGetSchema)
async def update_board_name(board_id: int, data: UpdateBoardNameSchema, db: Session = Depends(get_db)):
    board = get_object_or_404(db, Board, id=board_id)
    board.name = data.name
    Board.manager(db).update(board)
    return board
