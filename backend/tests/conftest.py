import os
import sys
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from ..core.config import settings
from ..db.models import jobs
from ..schemas.User import User_Create
from ..security.oauth2 import login_user
from .utils.Jobs import create_various_jobs
from .utils.Users import authentication_cookie
from .utils.Users import create_test_user

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


from backend.db.base import Base
from backend.db.database import get_db
from backend.apis.base import api_router


def start_aplication():
    app = FastAPI()
    app.include_router(api_router)
    return app


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def app() -> Generator[FastAPI, Any, None]:

    _app = start_aplication()
    yield _app


@pytest.fixture(scope="function")
def db_session() -> Generator[SessionTesting, Any, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionTesting()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    def get_test_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = get_test_db

    yield TestClient(app=app)


@pytest.fixture(scope="function")
def authorized_client(client: TestClient, test_user):
    cookie = authentication_cookie(client, test_user["email"], test_user["password"])
    client.cookies.set("Authorization", cookie)

    return client


@pytest.fixture(scope="function")
def create_jobs(db_session: Session, test_user):

    return create_various_jobs(test_user=test_user, db_session=db_session)


@pytest.fixture(scope="function")
def test_user(db_session: Session):
    return create_test_user(email=settings.test_email, db=db_session)
