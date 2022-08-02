from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.crud import BaseManager
from src.database import Base


class CustomBaseMixin:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class WorkoutMuscle(CustomBaseMixin, Base):
    __tablename__ = 'workout_muscles'

    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    muscle_id = Column(Integer, ForeignKey('muscles.id'))


class Workout(CustomBaseMixin, Base):
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    related_muscles = relationship('Muscle', secondary=WorkoutMuscle.__tablename__, backref='related_workouts')


Workout.manager = BaseManager(Workout)


class Muscle(CustomBaseMixin, Base):
    __tablename__ = 'muscles'

    id = Column(Integer, primary_key=True)
    name = Column(String)


Muscle.manager = BaseManager(Muscle)


class BoardWorkout(CustomBaseMixin, Base):
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


class Board(CustomBaseMixin, Base):
    __tablename__ = 'boards'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    created = Column(DateTime, default=datetime.now)

    board_workouts = relationship('BoardWorkout')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)


Board.manager = BaseManager(Board)


class User(CustomBaseMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password_hash = Column(String(63))
    first_name = Column(String(63))
    last_name = Column(String(63))
    created = Column(DateTime, default=datetime.now)

    boards = relationship('Board')


User.manager = BaseManager(User)
