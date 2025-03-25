from abc import ABCMeta

from ed_domain.entities.order import Order

from ed_core.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)
from ed_core.domain.entities.some_entity import SomeEntity


class ABCOrderRepository(
    ABCGenericRepository[Order],
    metaclass=ABCMeta,
): ...
