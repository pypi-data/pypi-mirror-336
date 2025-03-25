from typing import TypedDict
from uuid import UUID

from domain.entities.business import BillingDetail
from domain.services.core.dtos.location_dto import LocationDto


class BusinessDto(TypedDict):
    id: UUID
    business_name: str
    owner_first_name: str
    owner_last_name: str
    phone_number: str
    email: str
    location: LocationDto
    billing_details: list[BillingDetail]
