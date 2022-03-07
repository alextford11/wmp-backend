from typing import List, Union

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Query, Session

MODELS = Union['WorkoutMuscle', 'Workout', 'Muscle', 'BoardWorkout', 'Board']


class BaseManager:
    """
    Query handler to stop repeating code
    """

    model: Union[MODELS] = None

    def __init__(self, model=None):
        if not self.model:
            self.model = model

    def __call__(self, db: Session):
        self.db = db
        return self

    def get(self, **kwargs) -> Union[MODELS]:
        return self.db.query(self.model).filter_by(**kwargs).one()

    def filter(self, *args, **kwargs) -> Query:
        q = self.db.query(self.model)
        if args:
            q.filter(*args)
        if kwargs:
            q.filter_by(**kwargs)
        return q

    def all(self) -> List[Union[MODELS]]:
        return self.db.query(self.model).all()

    def count(self, **kwargs) -> int:
        return self.db.query(self.model).filter_by(**kwargs).count()

    def create(self, instance: Union[MODELS]) -> Union[MODELS]:
        assert not instance.id

        if hasattr(instance, 'pre_create'):
            instance.pre_create(db=self.db)
        try:
            self.db.add(instance)
            self.db.commit()
            self.db.flush()
        except IntegrityError:
            self.db.rollback()
            self.update(instance)

        if hasattr(instance, 'post_create'):
            instance.post_create(db=self.db)
        return instance

    def update(self, instance: Union[MODELS]):
        assert instance.id

        try:
            self.merge(instance)
        except IntegrityError:
            self.db.rollback()
        self.db.commit()
        self.db.flush()

    def merge(self, instance):
        self.db.merge(instance)
        self.db.commit()
        self.db.flush()

    def get_or_create(self, **kwargs) -> Union[MODELS]:
        try:
            instance = self.get(**kwargs)
        except NoResultFound:
            instance = self.create(**kwargs)
        return instance

    def create_or_update(self, instance: Union[MODELS]):
        if instance.id:
            return self.update(instance)
        return self.create(instance)

    def delete(self, *args, **kwargs) -> int:
        count = self.db.query(self.model).filter(*args).filter_by(**kwargs).delete()
        self.db.commit()
        self.db.flush()
        return count

    def create_many(self, *instances: List[Union[MODELS]]) -> None:
        self.db.add_all(*[instances])
        self.db.commit()

    def exists(self, **kwargs) -> bool:
        return bool(self.db.query(self.model).filter_by(**kwargs).first())


def get_object_or_404(db: Session, model: Union[MODELS], **kwargs):
    try:
        obj = db.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f'{model.__class__.__name__} Not Found')
    else:
        return obj
