from abc import ABCMeta

from ed_domain.entities import Location

from ed_core.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCLocationRepository(
    ABCGenericRepository[Location],
    metaclass=ABCMeta,
): ...
