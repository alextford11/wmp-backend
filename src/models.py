from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from crud import BaseManager


class WorkoutMuscle(Base):
    __tablename__ = 'workout_muscles'

    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    muscle_id = Column(Integer, ForeignKey('muscles.id'))


class Workout(Base):
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    muscles = relationship('Muscle', secondary=WorkoutMuscle.__tablename__, backref='workouts')


Workout.manager = BaseManager(Workout)


class Muscle(Base):
    __tablename__ = 'muscles'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    workouts = relationship('Workout', secondary=WorkoutMuscle.__tablename__, backref='muscles')


Muscle.manager = BaseManager(Muscle)


class BoardWorkout(Base):
    __tablename__ = 'board_workouts'

    id = Column(Integer, primary_key=True)
    sort_value = Column(Integer)
    board_id = Column(Integer, ForeignKey('boards.id'))
    workout_id = Column(Integer, ForeignKey('workouts.id'))

    workout = relationship('Workout')


class Board(Base):
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True)

    board_workouts = relationship('BoardWorkout')


Board.manager = BaseManager(Board)
