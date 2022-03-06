from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base
from src.crud import BaseManager


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

    workout = relationship('Workout')

    def pre_create(self, db):
        board = db.query(Board).get(self.board_id)
        self.sort_value = len(board.board_workouts) + 1


BoardWorkout.manager = BaseManager(BoardWorkout)


class Board(Base):
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True)

    board_workouts = relationship('BoardWorkout')


Board.manager = BaseManager(Board)
