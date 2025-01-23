from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_signup_user(db_session):
    response = client.post(
        "/v1/auth/signup",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    assert response.json()["message"] == "User registered successfully"
    assert response.json()["user"]["email"] == "newuser@example.com"


def test_obtain_token(db_session):
    # Assuming the user has already been created
    response = client.post(
        "/v1/auth/token/obtain",
        json={"username": "newuser", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_refresh_token(db_session):
    # Assuming valid tokens are provided
    refresh_token = "mock_refresh_token"
    response = client.post(
        "/v1/auth/token/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
