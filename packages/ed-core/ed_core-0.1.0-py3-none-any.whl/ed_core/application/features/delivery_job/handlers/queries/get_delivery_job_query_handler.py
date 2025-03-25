from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.contracts.infrastructure.persistence.abc_unit_of_work import \
    ABCUnitOfWork
from ed_core.application.features.business.dtos.order_dto import OrderDto
from ed_core.application.features.common.dtos import DeliveryJobDto
from ed_core.application.features.common.dtos.route_dto import RouteDto
from ed_core.application.features.delivery_job.requests.queries.get_delivery_job_query import \
    GetDeliveryJobQuery
from ed_core.common.exception_helpers import ApplicationException, Exceptions


@request_handler(GetDeliveryJobQuery, BaseResponse[DeliveryJobDto])
class GetDeliveryJobQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetDeliveryJobQuery
    ) -> BaseResponse[DeliveryJobDto]:
        if delivery_job := self._uow.delivery_job_repository.get(
            id=request.delivery_job_id
        ):
            return BaseResponse[DeliveryJobDto].success(
                "Delivery jobs fetched successfully.",
                DeliveryJobDto(
                    **delivery_job,
                    orders=[
                        OrderDto(
                            self._uow.order_repository.get(
                                id=order_id),  # type: ignore
                        )
                        for order_id in delivery_job["order_ids"]
                    ],
                    route=RouteDto(
                        self._uow.route_repository.get(
                            id=delivery_job["route_id"]
                        ),  # type: ignore
                    ),
                ),
            )

        raise ApplicationException(
            Exceptions.NotFoundException,
            "Delivery jobs not found.",
            [f"Delivery jobs for driver with id {request.delivery_job_id} not found."],
        )
