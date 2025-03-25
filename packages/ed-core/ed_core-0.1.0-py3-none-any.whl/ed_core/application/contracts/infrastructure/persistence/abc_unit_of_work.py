from abc import ABCMeta, abstractmethod

from ed_core.application.contracts.infrastructure.persistence.abc_bill_repository import (
    ABCBillRepository,
)
from ed_core.application.contracts.infrastructure.persistence.abc_business_repository import (
    ABCBusinessRepository,
)
from ed_core.application.contracts.infrastructure.persistence.abc_car_repository import (
    ABCCarRepository,
)
from ed_core.application.contracts.infrastructure.persistence.abc_consumer_repository import (
    ABCConsumerRepository,
)
from ed_core.application.contracts.infrastructure.persistence.abc_delivery_job_repository import (
    ABCDeliveryJobRepository,
)
from ed_core.application.contracts.infrastructure.persistence.abc_driver_repository import (
    ABCDriverRepository,
)
from ed_core.application.contracts.infrastructure.persistence.abc_location_repository import (
    ABCLocationRepository,
)
from ed_core.application.contracts.infrastructure.persistence.abc_order_repository import (
    ABCOrderRepository,
)
from ed_core.application.contracts.infrastructure.persistence.abc_route_repository import (
    ABCRouteRepository,
)


class ABCUnitOfWork(metaclass=ABCMeta):
    @property
    @abstractmethod
    def bill_repository(self) -> ABCBillRepository:
        pass

    @property
    @abstractmethod
    def business_repository(self) -> ABCBusinessRepository:
        pass

    @property
    @abstractmethod
    def car_repository(self) -> ABCCarRepository:
        pass

    @property
    @abstractmethod
    def consumer_repository(self) -> ABCConsumerRepository:
        pass

    @property
    @abstractmethod
    def delivery_job_repository(self) -> ABCDeliveryJobRepository:
        pass

    @property
    @abstractmethod
    def driver_repository(self) -> ABCDriverRepository:
        pass

    @property
    @abstractmethod
    def location_repository(self) -> ABCLocationRepository:
        pass

    @property
    @abstractmethod
    def order_repository(self) -> ABCOrderRepository:
        pass

    @property
    @abstractmethod
    def route_repository(self) -> ABCRouteRepository:
        pass
