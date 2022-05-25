from src.models import Board, BoardWorkout, Muscle, Workout
from src.settings import Settings


class Factory:
    def __init__(self, db, settings: Settings):
        self.db = db
        self.settings = settings

    def create_board(self):
        return Board.manager(self.db).create(Board())

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
