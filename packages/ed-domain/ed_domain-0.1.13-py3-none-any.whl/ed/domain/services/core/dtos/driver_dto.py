from typing import NotRequired, TypedDict

from ed.domain.services.core.dtos.car_dto import CarDto
from ed.domain.services.core.dtos.location_dto import LocationDto


class DriverDto(TypedDict):
    first_name: str
    last_name: str
    profile_image: str
    phone_number: str
    email: NotRequired[str]
    car: CarDto
    location: LocationDto
