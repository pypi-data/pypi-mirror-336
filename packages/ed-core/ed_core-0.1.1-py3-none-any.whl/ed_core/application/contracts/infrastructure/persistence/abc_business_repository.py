from abc import ABCMeta

from ed_domain.entities import Business

from ed_core.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCBusinessRepository(
    ABCGenericRepository[Business],
    metaclass=ABCMeta,
): ...
