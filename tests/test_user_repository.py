def test_create_user(db_session, user_repository):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "hashed_password": "hashedpassword",
    }
    user = user_repository.create(db_session, user_data)

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"


def test_get_user_by_email(db_session, user_repository):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "hashed_password": "hashedpassword",
    }
    user_repository.create(db_session, user_data)
    user = user_repository.get_by_email(db_session, "test@example.com")

    assert user is not None
    assert user.email == "test@example.com"
