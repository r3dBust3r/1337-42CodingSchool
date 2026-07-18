from typing import List, Tuple, Union, TYPE_CHECKING
from collections import deque

if TYPE_CHECKING:
    from graph import Graph
    from zone import Zone
    from drone import Drone
    from connection import Connection


class Simulator:
    """Simulate drone movement along the computed paths."""

    def __init__(
            self, graph: 'Graph',
            paths: List[Tuple[float, List['Zone']]]
    ) -> None:
        """Create a simulator for a graph and a set of candidate paths."""
        self.graph: 'Graph' = graph
        self.paths: List[Tuple[float, List['Zone']]] = paths
        self.turns: List[str] = []

        self._check_disconnected_graph()
        self._assign_paths_to_drones()

    def _assign_paths_to_drones(self) -> None:
        """Assign one of the available paths to each drone."""
        if not self.paths:
            raise ValueError(
                f'> No available paths to: {self.graph.end_zone.name}'
            )

        for d in self.graph.drones:
            d_id = int(d.id.replace('D', ''))
            d.path = self.paths[d_id % len(self.paths)]

    def _check_disconnected_graph(self) -> None:
        """Ensure every zone is reachable from the start zone."""
        start = self.graph.start_zone

        if not start:
            raise ValueError("> Graph has no start zone")

        dq = deque([start])
        checked = {start}

        while dq:
            current = dq.popleft()

            for nbr in current.neighbors:
                if nbr not in checked:
                    checked.add(nbr)
                    dq.append(nbr)

        if len(checked) != len(self.graph.zones):
            raise ValueError("> Graph contains unreachable zones")

    def run(self) -> None:
        """Execute the simulation turn by turn until all drones are delivered."""
        STOP_ON = 10_000
        keep_running = STOP_ON

        while not self._all_delivered() and keep_running:
            turns = ''
            conns_tracker = {
                c: len(c.current_drones) for c in self.graph.connections
            }
            for d in self.graph.drones:

                if d.delivered:
                    continue

                if d.path_index + 1 == len(d.path[1]):
                    continue

                cur_zone: 'Zone' = d.path[1][d.path_index]
                nxt_zone: 'Zone' = d.path[1][d.path_index + 1]

                conn: 'Connection' = self._get_conn(cur_zone, nxt_zone)

                if nxt_zone.zone in ['normal', 'priority']:

                    # next zone has no space
                    if len(nxt_zone.current_drones) == nxt_zone.max_drones:
                        continue

                    # connection has no space
                    if conns_tracker[conn] == conn.max_link_capacity:
                        continue

                    conns_tracker[conn] += 1

                    self._move_drone(d, cur_zone, nxt_zone)
                    turns += f'{d.id}-{nxt_zone.name} '

                elif nxt_zone.zone == 'restricted':
                    if d.in_transit:
                        self._move_drone(d, conn, nxt_zone)
                        turns += f'{d.id}-{nxt_zone.name} '
                        d.in_transit = False

                    else:
                        # next zone has no space
                        crr_ds = conn.current_drones
                        nxt_ds = nxt_zone.current_drones
                        if (len(crr_ds) + len(nxt_ds)) == nxt_zone.max_drones:
                            continue

                        # connection has no space
                        if conns_tracker[conn] == conn.max_link_capacity:
                            continue

                        conns_tracker[conn] += 1

                        self._move_drone(d, cur_zone, conn, False)
                        d.in_transit = True

                        turns += f'{d.id}-{conn.name} '

            self.turns.append(turns.strip())
            keep_running -= 1

        if len(self.turns) == STOP_ON:
            raise ValueError(f'Warning: Hit {STOP_ON} loop, had to exit!')

    def _all_delivered(self) -> bool:
        """Return whether every drone has reached the end zone."""
        end_drones = len(self.graph.end_zone.current_drones)
        return len(self.graph.drones) == end_drones

    def _move_drone(
            self,
            d: 'Drone',
            cur: Union['Zone', 'Connection'],
            nxt: Union['Zone', 'Connection'],
            to_zone: bool = True
    ) -> None:
        """Move a drone from one node to another and update tracking lists."""
        if to_zone:
            d.path_index += 1

        d.current_zone = nxt

        if d in cur.current_drones:
            cur.current_drones.remove(d)
        nxt.current_drones.append(d)

    def _get_conn(self, z1: 'Zone', z2: 'Zone') -> 'Connection':
        """Return the connection linking two zones."""
        for conn in self.graph.connections:
            if conn.name == f'{z1.name}-{z2.name}' or \
               conn.name == f'{z2.name}-{z1.name}':
                return conn
        raise ValueError("Connection not found")

    def display_turns(self) -> None:
        """Print the recorded turns and the total number of turns."""
        for t in self.turns:
            print(t)

        print(f'\nTotal turns: {len(self.turns)}')
