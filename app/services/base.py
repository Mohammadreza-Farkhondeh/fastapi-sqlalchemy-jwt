from typing import Generic, List, TypeVar

from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from app.schemas.base import BaseSchema

ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType", bound=BaseSchema)


class BaseService(Generic[ModelType, SchemaType]):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def get(self, db: Session, id: int) -> SchemaType:
        result = self.repository.get(db, id)
        if result is None:
            raise ValueError(f"Record with id {id} not found")
        return result

    def get_all(self, db: Session, skip: int = 0, limit: int = 10) -> List[SchemaType]:
        return self.repository.get_all(db, skip, limit)

    def create(self, db: Session, obj_in: SchemaType) -> ModelType:
        return self.repository.create(db, obj_in.dict())

    def update(self, db: Session, db_obj: ModelType, obj_in: SchemaType) -> ModelType:
        return self.repository.update(db, db_obj, obj_in.dict())

    def delete(self, db: Session, db_obj: ModelType) -> None:
        self.repository.delete(db, db_obj)
