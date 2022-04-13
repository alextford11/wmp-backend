from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.crud import BaseManager
from src.database import Base


class WorkoutMuscle(Base):
    __tablename__ = 'workout_muscles'

    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    muscle_id = Column(Integer, ForeignKey('muscles.id'))


class Workout(Base):
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    related_muscles = relationship('Muscle', secondary=WorkoutMuscle.__tablename__, backref='related_workouts')


Workout.manager = BaseManager(Workout)


class Muscle(Base):
    __tablename__ = 'muscles'

    id = Column(Integer, primary_key=True)
    name = Column(String)


Muscle.manager = BaseManager(Muscle)


class BoardWorkout(Base):
    __tablename__ = 'board_workouts'

    id = Column(Integer, primary_key=True)
    sort_value = Column(Integer, default=1)
    board_id = Column(Integer, ForeignKey('boards.id'))
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    sets_value = Column(Integer, default=3)
    reps_value = Column(Integer, default=10)
    measurement_value = Column(Integer, default=10)
    measurement_unit = Column(String, default='kg')

    workout = relationship('Workout')

    def pre_create(self, db):
        if not self.sort_value:
            self.set_sort_value(db)

    def set_sort_value(self, db):
        board = Board.manager(db).get(id=self.board_id)
        highest_value = len(board.board_workouts) + 1
        for board_workout in board.board_workouts:
            highest_value = max(highest_value, board_workout.sort_value + 1)
        self.sort_value = highest_value


BoardWorkout.manager = BaseManager(BoardWorkout)


class Board(Base):
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True)

    board_workouts = relationship('BoardWorkout')


Board.manager = BaseManager(Board)
