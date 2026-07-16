from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from zone import Zone
    from connection import Connection


class Drone:
    d_id: int = 1
    def __init__(self, end_zone: 'Zone') -> None:
        self.id: str = f'D{Drone.d_id}'
        self.current_zone: 'Zone' | 'Connection'
        self.path: Tuple[float, List[Zone]] = (0, [])
        self.path_index: int = 0
        self.end_zone: 'Zone' | None = end_zone
        self.in_transit: bool = False

        Drone.d_id += 1

    @property
    def delivered(self) -> bool:
        return self.current_zone == self.end_zone
