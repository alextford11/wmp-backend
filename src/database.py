from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.settings import Settings

Base = declarative_base()
settings = Settings()


def get_engine():
    return create_engine(settings.pg_dsn)


def get_session():
    engine = get_engine()
    session = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)
    engine.dispose()
    return session


SessionLocal = get_session()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
