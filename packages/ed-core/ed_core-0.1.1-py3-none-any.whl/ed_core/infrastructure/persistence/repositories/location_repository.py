from ed_domain.entities.location import Location

from ed_core.application.contracts.infrastructure.persistence import ABCLocationRepository
from ed_core.infrastructure.persistence.db_client import DbClient
from ed_core.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class LocationRepository(GenericRepository[Location], ABCLocationRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "location")
