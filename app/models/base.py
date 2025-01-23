from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
