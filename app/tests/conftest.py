import pytest
from fastapi.testclient import TestClient

from app.db.base import DBSessionMaker


@pytest.fixture()
def db():
    session = DBSessionMaker()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client():
    from app.main import app

    with TestClient(app) as c:
        yield c
