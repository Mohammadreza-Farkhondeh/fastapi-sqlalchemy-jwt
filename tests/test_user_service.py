from app.core.security import SecurityUtils
from app.schemas.user import UserCreate
from app.services.user_service import UserService


def test_create_user_success(db_session):
    user_service = UserService()
    user_data = UserCreate(
        username="testuser", email="test@example.com", password="securepassword"
    )
    user = user_service.create_user(db_session, user_data)

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert SecurityUtils.verify_password("securepassword", user.hashed_password)


def test_create_user_duplicate_email(db_session):
    user_service = UserService()
    user_data = UserCreate(
        username="testuser", email="test@example.com", password="securepassword"
    )
    user_service.create_user(db_session, user_data)

    try:
        user_service.create_user(db_session, user_data)
    except ValueError as e:
        assert str(e) == "Email is already registered."
