from abc import ABCMeta

from ed_domain.entities import Driver

from ed_core.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCDriverRepository(
    ABCGenericRepository[Driver],
    metaclass=ABCMeta,
): ...
