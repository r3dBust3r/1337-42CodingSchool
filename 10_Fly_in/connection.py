from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from drone import Drone


class Connection:
    """Represents a link between zones that can carry drones.

    A connection has a name, a maximum link capacity, and keeps track of the
    drones currently using it.
    """

    def __init__(self, name: str, max_link_capacity: int = 1) -> None:
        """Create a new connection.

        Args:
            name: Human-readable connection name.
            max_link_capacity: Maximum number of drones allowed on the link.
        """
        self.name: str = name
        self.max_link_capacity: int = max_link_capacity
        self.current_drones: List['Drone'] = []

    def __str__(self) -> str:
        """Return a compact string representation of the connection."""
        return f"{self.name} ({self.max_link_capacity})"
