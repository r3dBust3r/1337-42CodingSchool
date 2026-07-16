from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from drone import Drone


class Connection:
    def __init__(self, name: str, max_link_capacity: int = 1) -> None:
        self.name: str = name
        self.max_link_capacity: int = max_link_capacity
        self.current_drones: List['Drone'] = []

    def __str__(self) -> str:
        return f"{self.name} ({self.max_link_capacity})"
