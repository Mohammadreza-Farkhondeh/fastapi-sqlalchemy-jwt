from sqlalchemy.orm import Session

from app.core.security import SecurityUtils
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.services.base import BaseService


class UserService(BaseService[User, UserCreate]):
    def __init__(self):
        super().__init__(UserRepository())

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        """
        Creates a new user with a hashed password.
        """
        # Check if email is already in use
        existing_user = self.repository.get_by_email(db, email=user_in.email)
        if existing_user:
            raise ValueError("Email is already registered.")

        # Hash the password before saving
        user_in.hashed_password = SecurityUtils.hash_password(user_in.password)
        del user_in.password  # Remove plain-text password for security

        return self.repository.create(db, user_in.model_dump())

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
