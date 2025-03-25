from ed_domain.entities import Car

from ed_core.application.contracts.infrastructure.persistence import ABCCarRepository
from ed_core.infrastructure.persistence.db_client import DbClient
from ed_core.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class CarRepository(GenericRepository[Car], ABCCarRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "car")
