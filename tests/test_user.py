import uuid

from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)

USER_URL = "/api/v1/user"


def unique_email():
    return f"user_{uuid.uuid4().hex}@test.local"


def test_get_existed_user():
    email = unique_email()
    data = {
        "name": "Test User",
        "email": email
    }

    create_response = client.post(USER_URL, json=data)
    assert create_response.status_code == 201

    response = client.get(USER_URL, params={"email": email})

    assert response.status_code == 200
    assert response.json()["name"] == data["name"]
    assert response.json()["email"] == data["email"]
    assert "id" in response.json()


def test_get_not_existed_user():
    email = unique_email()

    response = client.get(USER_URL, params={"email": email})

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found"
    }


def test_create_user():
    email = unique_email()
    data = {
        "name": "Test User",
        "email": email
    }

    response = client.post(USER_URL, json=data)

    assert response.status_code == 201
    assert isinstance(response.json(), int)


def test_create_user_with_existing_email():
    email = unique_email()
    data = {
        "name": "Test User",
        "email": email
    }

    first_response = client.post(USER_URL, json=data)
    second_response = client.post(USER_URL, json=data)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "User with this email already exists"
    }


def test_delete_user():
    email = unique_email()
    data = {
        "name": "Test User",
        "email": email
    }

    create_response = client.post(USER_URL, json=data)
    assert create_response.status_code == 201

    delete_response = client.delete(USER_URL, params={"email": email})

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(USER_URL, params={"email": email})
    assert get_response.status_code == 404
