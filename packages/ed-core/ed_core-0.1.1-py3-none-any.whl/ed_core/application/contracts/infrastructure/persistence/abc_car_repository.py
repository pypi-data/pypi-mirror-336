from abc import ABCMeta

from ed_domain.entities import Car

from ed_core.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCCarRepository(
    ABCGenericRepository[Car],
    metaclass=ABCMeta,
): ...
