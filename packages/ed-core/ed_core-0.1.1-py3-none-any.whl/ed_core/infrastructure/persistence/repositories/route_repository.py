from ed_domain.entities.route import Route

from ed_core.application.contracts.infrastructure.persistence import ABCRouteRepository
from ed_core.infrastructure.persistence.db_client import DbClient
from ed_core.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class RouteRepository(GenericRepository[Route], ABCRouteRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "route")
