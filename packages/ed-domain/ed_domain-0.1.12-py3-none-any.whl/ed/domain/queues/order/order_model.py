from datetime import datetime
from typing import TypedDict
from uuid import UUID

from domain.entities.order import OrderStatus, Parcel
from domain.queues.order.business_model import BusinessModel
from domain.queues.order.consumer_model import ConsumerModel


class OrderModel(TypedDict):
    id: UUID
    consumer: ConsumerModel
    business: BusinessModel
    bill_id: UUID
    latest_time_of_delivery: datetime
    parcel: Parcel
    order_status: OrderStatus
