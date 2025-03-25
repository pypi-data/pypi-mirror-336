from ed_domain.entities.order import Order

from ed_core.application.contracts.infrastructure.persistence import ABCOrderRepository
from ed_core.infrastructure.persistence.db_client import DbClient
from ed_core.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class OrderRepository(GenericRepository[Order], ABCOrderRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "order")
