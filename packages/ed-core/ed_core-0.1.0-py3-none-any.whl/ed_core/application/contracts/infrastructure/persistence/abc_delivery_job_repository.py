from abc import ABCMeta

from ed_domain.entities import DeliveryJob

from ed_core.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCDeliveryJobRepository(
    ABCGenericRepository[DeliveryJob],
    metaclass=ABCMeta,
): ...
