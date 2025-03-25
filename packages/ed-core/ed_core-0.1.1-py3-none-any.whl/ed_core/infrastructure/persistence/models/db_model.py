from typing import Generic, TypeVar

TEntity = TypeVar("TEntity")


class DbModel(Generic[TEntity]):
    @classmethod
    def from_entity(cls, entity: TEntity) -> "DbModel":
        """Convert a business entity to a database model."""
        ...

    @staticmethod
    def to_entity(model: "DbModel") -> TEntity:
        """Convert a database model to a business entity."""
        ...
