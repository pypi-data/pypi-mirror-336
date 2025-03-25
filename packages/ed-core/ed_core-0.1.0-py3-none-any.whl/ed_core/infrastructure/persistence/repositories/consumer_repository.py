from ed_domain.entities import Consumer

from ed_core.application.contracts.infrastructure.persistence import ABCConsumerRepository
from ed_core.infrastructure.persistence.db_client import DbClient
from ed_core.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class ConsumerRepository(GenericRepository[Consumer], ABCConsumerRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "consumer")
