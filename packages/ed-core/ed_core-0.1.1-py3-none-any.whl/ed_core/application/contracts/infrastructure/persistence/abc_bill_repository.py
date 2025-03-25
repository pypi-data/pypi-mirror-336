from abc import ABCMeta

from ed_domain.entities import Bill

from ed_core.application.contracts.infrastructure.persistence.abc_generic_repository import (
    ABCGenericRepository,
)


class ABCBillRepository(
    ABCGenericRepository[Bill],
    metaclass=ABCMeta,
): ...
