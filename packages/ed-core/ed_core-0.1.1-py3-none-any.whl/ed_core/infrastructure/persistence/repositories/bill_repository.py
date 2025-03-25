from ed_domain.entities import Bill

from ed_core.application.contracts.infrastructure.persistence import ABCBillRepository
from ed_core.infrastructure.persistence.db_client import DbClient
from ed_core.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class BillRepository(GenericRepository[Bill], ABCBillRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "bill")
