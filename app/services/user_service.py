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
        # Check if email is already in use
        existing_user = self.repository.get_by_email(db, email=user_in.email)
        if existing_user:
            raise ValueError("Email is already registered.")

        # Hash the password before saving
        user_in.hashed_password = SecurityUtils.hash_password(user_in.password)
        del user_in.password

        return self.repository.create(db, user_in.model_dump())
