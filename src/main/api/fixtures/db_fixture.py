import pytest
from src.main.api.db.engine import SessionLocal, engine
from src.main.api.db.crud.user_crud import UserCrudDb as User


@pytest.fixture(scope = "function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind = connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
