from ed_domain.entities import Driver

from ed_core.application.contracts.infrastructure.persistence import ABCDriverRepository
from ed_core.infrastructure.persistence.db_client import DbClient
from ed_core.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class DriverRepository(GenericRepository[Driver], ABCDriverRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "driver")
