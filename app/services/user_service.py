from sqlalchemy.orm import Session

from app.core.security import SecurityUtils
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserOut
from app.services.base import BaseService


class UserService(BaseService[User, UserCreate]):
    def __init__(self):
        super().__init__(UserRepository())
        self.repository: UserRepository

    def create_user(self, db: Session, user_in: UserCreate) -> UserOut:
        """
        Creates a new user with a hashed password.
        """
        existing_user = self.repository.get_by_email(db, email=user_in.email)
        if existing_user:
            raise ValueError("Email is already registered.")

        user = {
            "username": user_in.username,
            "email": user_in.email,
            "hashed_password": SecurityUtils.hash_password(user_in.password),
        }

        user = self.repository.create(db, user)
        return UserOut(**user.__dict__)

    def authenticate_user(self, db: Session, email: str, password: str) -> User | None:
        """
        Authenticates a user by email and password.

        Returns:
            User object if authentication is successful, otherwise None.
        """
        user = self.repository.get_by_email(db, email=email)
        if not user:
            return None  # User not found

        if not SecurityUtils.verify_password(password, user.hashed_password):
            return None  # Password does not match

        return user  # Authentication successful
