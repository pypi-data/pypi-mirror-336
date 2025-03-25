from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

from ed_core.domain.entities.some_entity import SomeEntity
from ed_core.infrastructure.persistence.db_client import DbClient
from ed_core.infrastructure.persistence.models.db_model import DbModel

db = DbClient()


class SomeEntityModel(db.Base, DbModel[SomeEntity]):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    age = Column(Integer)

    @classmethod
    def from_entity(cls, entity: SomeEntity) -> "SomeEntityModel":
        return cls(entity.name, entity.email, entity.age)

    @staticmethod
    def to_entity(model: "SomeEntityModel") -> SomeEntity:
        return SomeEntity(id=0, name=str(model.name), email=str(model.email), age=0)
