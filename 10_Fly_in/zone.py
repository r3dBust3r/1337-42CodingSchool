from typing import List
from drone import Drone


class Zone:
    def __init__(
            self, name: str, x: int, y: int, color: str = 'none',
            max_drones: int = 1, hub_type: str = 'hub', zone: str = 'normal'
    ) -> None:
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.color: str = color
        self.max_drones: int = max_drones
        self.hub_type: str = hub_type
        self.zone: str = zone
        self.neighbors: List['Zone'] = []
        self.move_cost: float = 0
        self.current_drones: List[Drone] = []

        if zone == 'normal':
            self.move_cost = 1.0
        elif zone == 'priority':
            self.move_cost = 0.999
        elif zone == 'restricted':
            self.move_cost = 2.0
        elif zone == 'blocked':
            self.move_cost = float('INF')

    def __str__(self) -> str:
        return (
            f"{self.name.capitalize()} ({self.zone}): ({self.x}, {self.y})"
            f", Color={self.color}, MAX={self.max_drones}"
            f", Neighbors: {[n.name for n in self.neighbors]} "
            f"({len(self.neighbors)})"
        )

    def add_neighbor(self, neighbor: 'Zone') -> None:
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
