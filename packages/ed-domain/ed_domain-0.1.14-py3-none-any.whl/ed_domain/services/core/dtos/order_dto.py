from datetime import datetime
from typing import NotRequired, TypedDict
from uuid import UUID

from ed_domain.entities.order import OrderStatus, Parcel
from ed_domain.services.core.dtos.consumer_dto import ConsumerDto


class OrderDto(TypedDict):
    id: UUID
    consumer: ConsumerDto
    latest_time_of_delivery: datetime
    parcel: Parcel
    order_status: OrderStatus
    delivery_job_id: NotRequired[UUID]
