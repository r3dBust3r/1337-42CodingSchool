from zone import Zone
from connection import Connection
from drone import Drone
from itertools import count
import heapq


class Graph:
    def __init__(self, zones, connections, nb_drones):
        self.zones       = []
        self.connections = []
        self.start_zone  = None
        self.end_zone    = None
        self.drones      = []


        for zone in zones:
            name        = zone['name']
            x           = zone['x']
            y           = zone['y']
            hub_type    = zone['hub_type']

            try: color      = zone['metadata']['color']
            except KeyError: color = 'none'
            
            try: max_drones = zone['metadata']['max_drones']
            except KeyError: max_drones = 1

            try: zone_type  = zone['metadata']['zone']
            except KeyError: zone_type = 'normal'

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
            name                = conn['name']
            max_link_capacity   = conn['metadata']['max_link_capacity']

            self.connections.append(
                Connection(
                    name=name,
                    max_link_capacity=max_link_capacity
                )
            )


        for z in self.zones:
            if z.hub_type == 'start_hub': self.start_zone = z
            if z.hub_type == 'end_hub': self.end_zone = z

        self.drones = [Drone(self.end_zone) for _ in range(nb_drones)]

        self.start_zone.max_drones = len(self.drones)
        self.end_zone.max_drones = len(self.drones)


    def create_graph(self):
        for d in self.drones:
            d.current_zone = self.start_zone
            self.start_zone.current_drones.append(d)

        for conn in self.connections:
            if '-' not in conn.name:
                raise ValueError('Invalid connection name!')

            start, end = conn.name.split('-')

            start = self._find_zone_by_name(start)
            end   = self._find_zone_by_name(end)

            if not start or not end:
                raise ValueError(f'Invalid connection between ({start} <-> {end})')

            start.add_neighbor(end)
            end.add_neighbor(start)


    def _find_zone_by_name(self, name):
        for zone in self.zones:
            if zone.name == name:
                return zone
        return None


    def find_multiple_paths(self):
        all_paths = []
        max_paths = 2
        counter = count()

        heap = [(0, next(counter), [self.start_zone])]

        while heap and len(all_paths) < max_paths:
            path_cost, _, current_path = heapq.heappop(heap)
            current_zone = current_path[-1]

            if current_zone == self.end_zone:
                all_paths.append((path_cost, current_path))
                continue

            neighbors = current_zone.neighbors

            for neighbor in neighbors:
                if neighbor in current_path or neighbor.zone == 'blocked':
                    continue

                new_path_cost = path_cost + neighbor.move_cost
                new_path = current_path + [neighbor]
                heapq.heappush(heap, (new_path_cost, next(counter), new_path))

        return all_paths
