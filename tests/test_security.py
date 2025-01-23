from datetime import timedelta

from app.core.security import SecurityUtils


def test_hash_password():
    password = "strongpassword123"
    hashed = SecurityUtils.hash_password(password)
    assert SecurityUtils.verify_password(password, hashed)


def test_create_access_token():
    data = {"sub": "testuser"}
    token = SecurityUtils.create_access_token(data)
    payload = SecurityUtils.verify_token(token)
    assert payload["sub"] == "testuser"


def test_expired_token():
    data = {"sub": "testuser"}
    token = SecurityUtils.create_access_token(data, expires_delta=timedelta(seconds=-1))
    payload = SecurityUtils.verify_token(token)
    assert payload is None
