from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ...db.repository.users import create_new_user
from ...db.repository.users import get_user_by_email
from ...schemas.User import User_Create


def authentication_cookie(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}

    res = client.post("/login", data=data)

    cookie = res.cookies.get("Authentication")

    res_cookie = cookie
    return res_cookie


def create_test_user(email: str, db: Session):
    password = "password123"
    user = {"username": email, "email": email, "password": password}

    user_created = User_Create(**user)
    user_get = create_new_user(user_created, db)

    user["id"] = user_get.id

    return user
