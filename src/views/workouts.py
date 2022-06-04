from fastapi import APIRouter, Depends
from requests import Session

from src.database import get_db
from src.models import Workout
from src.schemas.forms import SelectGroupInputListSchema
from src.schemas.workouts import WorkoutListSchema

router = APIRouter(prefix='/workouts')


@router.get('/list/', response_model=WorkoutListSchema)
def workout_list(db: Session = Depends(get_db)):
    return {'workouts': Workout.manager(db).all()}


@router.get('/list/grouped/', response_model=SelectGroupInputListSchema)
def workout_list_grouped(db: Session = Depends(get_db)):
    workouts = Workout.manager(db).order_by(Workout.name).all()

    muscle_workouts = {}
    for workout in workouts:
        related_muscles = workout.related_muscles
        for muscle in related_muscles:
            if muscle.name in muscle_workouts:
                muscle_workouts[muscle.name].append(workout)
            else:
                muscle_workouts[muscle.name] = [workout]
    options = [
        {
            'label': _muscle_name,
            'options': [{'label': _workout.name, 'value': _workout.id} for _workout in _muscle_workouts],
        }
        for _muscle_name, _muscle_workouts in dict(sorted(muscle_workouts.items())).items()
    ]
    return {'options': options}
