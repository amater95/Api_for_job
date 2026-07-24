from typing import Generic, TypeVar
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseCrud(Generic[ModelType]):
    model = None

    @classmethod
    def get_one_from_db(cls, db: Session, **filters) -> ModelType | None:
        return (db.query(cls.model).filter_by(**filters).first())

    @classmethod
    def count(cls, db: Session, **filters) -> int:
        return (db.query(cls.model).filter_by(**filters).count())
