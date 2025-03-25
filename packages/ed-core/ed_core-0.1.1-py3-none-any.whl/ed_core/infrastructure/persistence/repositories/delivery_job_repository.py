from ed_domain.entities import DeliveryJob

from ed_core.application.contracts.infrastructure.persistence import (
    ABCDeliveryJobRepository,
)
from ed_core.infrastructure.persistence.db_client import DbClient
from ed_core.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


class DeliveryJobRepository(GenericRepository[DeliveryJob], ABCDeliveryJobRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "delivery_job")
