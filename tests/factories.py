from datetime import timedelta

from src.auth import create_access_token, get_password_hash
from src.models import Board, BoardWorkout, Muscle, User, Workout
from src.settings import Settings


class Factory:
    def __init__(self, db, settings: Settings):
        self.db = db
        self.settings = settings

    def create_board(self, user_id: int = None):
        return Board.manager(self.db).create(Board(user_id=user_id))

    def create_muscle(self, name: str = 'Bicep'):
        return Muscle.manager(self.db).create(Muscle(name=name))

    def create_workout(self, name: str = 'Bench Press', muscles: list = None):
        muscles = muscles or []
        workout = Workout(name=name)
        for muscle in muscles:
            workout.related_muscles.append(muscle)
        return Workout.manager(self.db).create(workout)

    def create_board_workout(
        self,
        board: Board = None,
        workout: Workout = None,
        sort_value: int = None,
        sets_value: int = 3,
        reps_value: int = 10,
        measurement_value: int = 10,
        measurement_unit: str = 'kg',
    ):
        board = board or self.create_board()
        workout = workout or self.create_workout()
        return BoardWorkout.manager(self.db).create(
            BoardWorkout(
                board_id=board.id,
                workout_id=workout.id,
                sort_value=sort_value,
                sets_value=sets_value,
                reps_value=reps_value,
                measurement_value=measurement_value,
                measurement_unit=measurement_unit,
            )
        )

    def create_user(
        self,
        email: str = 'testing@example.com',
        first_name: str = 'Billy',
        last_name: str = 'Holiday',
        password: str = 'testing',
    ):
        user_data = dict(
            email=email,
            password_hash=get_password_hash(password) if password is not None else None,
            first_name=first_name,
            last_name=last_name,
        )
        user = User.manager(self.db).create(User(**user_data))
        return user

    def get_user_access_token(self, user):
        access_token_expires = timedelta(seconds=self.settings.auth_access_token_expiry_seconds)
        return create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
