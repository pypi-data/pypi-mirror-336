from datetime import datetime
from typing import TypedDict
from uuid import UUID

from domain.entities.driver_payment import Detail, DriverPaymentStatus


class DriverPaymentDto(TypedDict):
    id: UUID
    amount: float
    status: DriverPaymentStatus
    date: datetime
    detail: Detail
