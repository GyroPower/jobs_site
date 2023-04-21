from typing import Any
from typing import Generator
from ..db.models import jobs
from ..security.oauth2 import login_user
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings
import sys
import os
from sqlalchemy.orm import Session

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
    yield session


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session) -> Generator[TestClient, Any, None]:
    def get_test_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app=app) as client:
        print
        yield client


@pytest.fixture(scope="function")
def test_user(client: TestClient):
    user = {"username": "user1", "email": "other@example.com", "password": "1234"}

    res = client.post("/users/register/", json=user)
    user_res = res.json()
    user_res["password"] = user["password"]

    return user_res


@pytest.fixture(scope="function")
def token(test_user):
    return login_user.create_access_token(data={"user_id": test_user["id"]})


@pytest.fixture(scope="function")
def authorized_client(client: TestClient, token):

    client.cookies.set("Authorization", token)

    return client


@pytest.fixture()
def create_jobs(test_user, db_session: Session):
    data = [
        {
            "title": "company1",
            "company": "doogle",
            "company_url": "www.doogle.com",
            "location": "USA,NY",
            "description": "python",
        },
        {
            "title": "company2",
            "company": "foogle",
            "company_url": "www.foogle.com",
            "location": "USA,LA",
            "description": "python",
        },
        {
            "title": "company3",
            "company": "poogle",
            "company_url": "www.poogle.com",
            "location": "USA,NY",
            "description": "python",
        },
    ]

    def create_jobs_(job):
        return jobs.Jobs(**job, owner_id=test_user["id"])

    jobs_map = map(create_jobs_, data)
    jobs_list = list(jobs_map)
    db_session.add_all(jobs_list)
    db_session.commit()
    return db_session.query(jobs.Jobs).all()
