import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.database import Base, get_db
from src.settings import Settings
from tests.factories import Factory

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
    settings = Settings(dev_mode=False, pg_dsn=DB_DSN)
    assert not settings.dev_mode

    yield settings


@pytest.fixture(name='db')
def db_setup():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield from override_get_db()


@pytest.fixture
def client(db):
    # pass db through so db resets between tests
    with TestClient(app) as cli:
        return cli


@pytest.fixture
def factory(db, settings):
    return Factory(db, settings)
