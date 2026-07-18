from zone import Zone
from connection import Connection
from drone import Drone
from itertools import count
import heapq
from typing import List, Dict, Any, Tuple


class Graph:
    """Builds and analyzes the drone routing graph."""

    def __init__(
            self,
            zones: List[Dict[str, Any]],
            connections: List[Dict[str, Any]],
            nb_drones: int
    ) -> None:
        """Initialize zones, connections, and drones from raw input data."""
        self.zones: List[Zone] = []
        self.connections: List[Connection] = []
        self.start_zone: Zone
        self.end_zone: Zone
        self.drones: List[Drone] = []

        for zone in zones:
            name = zone['name']
            x = zone['x']
            y = zone['y']
            hub_type = zone['hub_type']

            try:
                color = zone['metadata']['color']
            except KeyError:
                color = 'none'

            try:
                max_drones = zone['metadata']['max_drones']
            except KeyError:
                max_drones = 1

            try:
                zone_type = zone['metadata']['zone']
            except KeyError:
                zone_type = 'normal'

            self.zones.append(
                Zone(
                    name=name,
                    x=x,
                    y=y,
                    hub_type=hub_type,
                    color=color,
                    max_drones=max_drones,
                    zone=zone_type
                )
            )

        for conn in connections:
            name = conn['name']
            max_link_capacity = conn['metadata']['max_link_capacity']

            self.connections.append(
                Connection(
                    name=name,
                    max_link_capacity=max_link_capacity
                )
            )

        for z in self.zones:
            if z.hub_type == 'start_hub':
                self.start_zone = z
            if z.hub_type == 'end_hub':
                self.end_zone = z

        assert self.end_zone is not None
        self.drones = [Drone(self.end_zone) for _ in range(nb_drones)]

        assert self.start_zone is not None
        assert self.end_zone is not None

        self.start_zone.max_drones = len(self.drones)
        self.end_zone.max_drones = len(self.drones)

    def create_graph(self) -> None:
        """Link zones together and place drones at the start zone."""
        for d in self.drones:
            d.current_zone = self.start_zone

            assert self.start_zone is not None
            self.start_zone.current_drones.append(d)

        for conn in self.connections:
            if '-' not in conn.name:
                raise ValueError('Invalid connection name!')

            start_name, end_name = conn.name.split('-')

            start = self._find_zone_by_name(start_name)
            end = self._find_zone_by_name(end_name)

            if not start or not end:
                raise ValueError(
                    f'Invalid connection between ({start} <-> {end})'
                )

            start.add_neighbor(end)
            end.add_neighbor(start)

    def _find_zone_by_name(self, name: str) -> Zone:
        """Return the zone with the given name."""
        for zone in self.zones:
            if zone.name == name:
                return zone
        raise ValueError("Zone not found")

    def find_multiple_paths(self) -> List[Tuple[float, List[Zone]]]:
        """Return up to the lowest-cost paths from the start zone to the end zone."""
        all_paths: List[Tuple[float, List[Zone]]] = []
        max_paths = 2
        counter = count()

        assert self.start_zone is not None

        heap: List[Tuple[float, int, List[Zone]]] = [
            (0, next(counter), [self.start_zone])
        ]

        while heap and len(all_paths) < max_paths:
            path_cost, _, current_path = heapq.heappop(heap)
            current_zone: Zone = current_path[-1]

            if current_zone == self.end_zone:
                all_paths.append((path_cost, current_path))
                continue

            neighbors: List[Zone] = current_zone.neighbors

            for neighbor in neighbors:
                if neighbor in current_path or neighbor.zone == 'blocked':
                    continue

                new_path_cost: float = path_cost + neighbor.move_cost
                new_path: List[Zone] = current_path + [neighbor]
                heapq.heappush(heap, (new_path_cost, next(counter), new_path))

        return all_paths
