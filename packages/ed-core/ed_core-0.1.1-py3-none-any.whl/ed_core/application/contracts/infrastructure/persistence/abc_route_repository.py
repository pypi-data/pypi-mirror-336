from abc import ABCMeta

from ed_domain.entities import Route

from ed_core.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCRouteRepository(
    ABCGenericRepository[Route],
    metaclass=ABCMeta,
): ...
