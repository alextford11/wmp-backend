from fastapi import APIRouter, Depends
from requests import Session

from src.database import get_db
from src.models import Workout
from src.schemas import WorkoutListSchema

router = APIRouter(prefix='/workouts')


@router.get('/list/', response_model=WorkoutListSchema)
def workout_list(db: Session = Depends(get_db)):
    return {'workouts': Workout.manager(db).all()}
