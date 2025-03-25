from typing import TypedDict

from domain.entities.route import WayPoint


class CreateRouteDto(TypedDict):
    waypoints: list[WayPoint]
    estimated_distance_in_kms: float
    estimated_time_in_minutes: int
