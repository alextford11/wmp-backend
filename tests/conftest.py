import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.database import Base, get_db
from src.models import Board, Workout, Muscle, BoardWorkout
from src.settings import Settings

DB_DSN = os.getenv('DATABASE_URL', 'postgresql://postgres@localhost:5432/wmp_backend_test')
engine = create_engine(DB_DSN)


def override_get_db():
    try:
        db = sessionmaker(autoflush=False, bind=engine)()
        yield db
    finally:
        db.close()
        engine.dispose()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(name='settings')
def settings_setup():
    settings = Settings(dev_mode=False, test_mode=True, pg_dsn=DB_DSN)
    assert not settings.dev_mode

    yield settings


@pytest.fixture(name='db')
def db_setup():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield from override_get_db()


@pytest.fixture
def client():
    with TestClient(app) as cli:
        return cli


def _create_board(db) -> Board:
    return Board.manager(db).create(Board())


@pytest.fixture(name='board')
def create_board(db) -> Board:
    return _create_board(db)


def create_muscle(db, **kwargs) -> Muscle:
    return Muscle.manager(db).create(Muscle(**kwargs))


def create_workout(db, **kwargs) -> Workout:
    muscles = kwargs.pop('muscles', [])
    workout = Workout(**kwargs)
    for muscle in muscles:
        workout.related_muscles.append(muscle)
    return Workout.manager(db).create(workout)


def create_board_workout(db, **kwargs) -> BoardWorkout:
    return BoardWorkout.manager(db).create(BoardWorkout(**kwargs))


def create_basic_board_workout(db, board=None) -> BoardWorkout:
    if not board:
        board = _create_board(db)
    muscle = create_muscle(db, name='Bicep')
    workout = create_workout(db, name='Pull Up', muscles=[muscle])
    return create_board_workout(db, board_id=board.id, workout_id=workout.id)
