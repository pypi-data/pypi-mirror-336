from abc import ABCMeta

from ed_domain.entities import Consumer

from ed_core.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCConsumerRepository(
    ABCGenericRepository[Consumer],
    metaclass=ABCMeta,
): ...
