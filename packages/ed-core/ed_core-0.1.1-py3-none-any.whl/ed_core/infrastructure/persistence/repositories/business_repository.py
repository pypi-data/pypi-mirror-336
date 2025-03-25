from ed_domain.entities import Business

from ed_core.application.contracts.infrastructure.persistence import ABCBusinessRepository
from ed_core.infrastructure.persistence.db_client import DbClient
from ed_core.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class BusinessRepository(GenericRepository[Business], ABCBusinessRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "business")
