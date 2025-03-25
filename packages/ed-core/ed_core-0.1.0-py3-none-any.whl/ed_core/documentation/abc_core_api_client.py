from abc import ABCMeta, abstractmethod

from ed_domain.services.common.api_response import ApiResponse

from ed_core.application.features.business.dtos import (CreateBusinessDto,
                                                        CreateOrderDto,
                                                        OrderDto)
from ed_core.application.features.common.dtos import (BusinessDto,
                                                      DeliveryJobDto,
                                                      DriverDto)
from ed_core.application.features.delivery_job.dtos.create_delivery_job_dto import \
    CreateDeliveryJobDto
from ed_core.application.features.driver.dtos import CreateDriverDto


class ABCCoreApiClient(metaclass=ABCMeta):
    @abstractmethod
    def create_driver(
        self, create_driver_dto: CreateDriverDto
    ) -> ApiResponse[DriverDto]: ...

    @abstractmethod
    def get_driver_delivery_jobs(
        self, driver_id: str
    ) -> ApiResponse[list[DeliveryJobDto]]: ...

    @abstractmethod
    def upload_driver_profile(
        self, driver_id: str) -> ApiResponse[DriverDto]: ...

    @abstractmethod
    def get_driver(self, driver_id: str) -> ApiResponse[DriverDto]: ...

    @abstractmethod
    def get_all_businesses(self) -> ApiResponse[list[BusinessDto]]: ...

    @abstractmethod
    def create_business(
        self, create_business_dto: CreateBusinessDto
    ) -> ApiResponse[BusinessDto]: ...

    @abstractmethod
    def get_business(self, business_id: str) -> ApiResponse[BusinessDto]: ...

    @abstractmethod
    def get_business_orders(
        self, business_id: str) -> ApiResponse[list[OrderDto]]: ...

    @abstractmethod
    def create_business_order(
        self, business_id: str, create_order_dto: CreateOrderDto
    ) -> ApiResponse[OrderDto]: ...

    @abstractmethod
    def get_delivery_jobs(self) -> ApiResponse[list[DeliveryJobDto]]: ...

    @abstractmethod
    def get_delivery_job(
        self, delivery_job_id: str) -> ApiResponse[DeliveryJobDto]: ...

    @abstractmethod
    def create_delivery_job(
        self, create_delivery_job_dto: CreateDeliveryJobDto
    ) -> ApiResponse[DeliveryJobDto]: ...
