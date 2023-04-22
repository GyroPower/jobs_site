import json

from fastapi.testclient import TestClient

from backend.schemas.User import User_Create


def test_create_user(client: TestClient):
    user = {"username": "user1", "email": "other@example.com", "password": "1234"}
    res = client.post("/users/register/", json=user)

    assert res.status_code == 200
    assert res.json().get("email") == user["email"]


def test_login(client: TestClient, test_user: User_Create):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert res.json().get("msg") == "success"


def test_authenticate(authorized_client: TestClient, test_user: User_Create):
    res = authorized_client.get("/users/me/")

    assert res.status_code == 200
    assert res.json().get("email") == test_user["email"]
