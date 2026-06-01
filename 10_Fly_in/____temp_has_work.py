# dron.py
class Drone:
    id = 1
    def __init__(self):
        self.id   = Drone.id
        self.zone = None
        Drone.id += 1


    def __str__(self):
        return str(self.id)



# zone.py
class Zone:
    def __init__(self, name, x, y, color='none', max_drones=1, type='hub', zone='normal'):
        self.name       = name
        self.x          = x
        self.y          = y
        self.color      = color
        self.max_drones = max_drones
        self.type       = type
        self.zone       = zone
        self.neighbors  = []
        self.move_cost  = 0
        self.drones     = []
        
        if   zone in ['normal', 'priority']:    self.move_cost = 1
        elif zone == 'restricted':              self.move_cost = 2
        elif zone == 'blocked':                 self.move_cost = 9e9


    def __str__(self):
        return (
            f"{self.name.capitalize()} ({self.zone}): ({self.x}, {self.y})"
            f", Color={self.color}, MAX={self.max_drones}"
            f", Neighbors: {[n.name for n in self.neighbors]} "
            f"({len(self.neighbors)})"
        )


    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)


    def move_drone(self, drone, to):
        self.remove(drone)
        to.append(drone)
        drone.zone = to





# main.py
from pydantic import BaseModel, ValidationError, Field
from typing import Literal, Dict, Optional
from zone import Zone
from drone import Drone
from connection import Connection
from graph import Graph
from collections import deque
from itertools import count
import heapq



class ZoneMetadata(BaseModel):
    color: Optional[str] = None
    max_drones: Optional[int] = None
    zone: Literal['normal', 'blocked', 'restricted', 'priority'] = 'normal'


class ZoneModel(BaseModel):
    type: Literal['start_hub', 'hub', 'end_hub']
    name: str = Field(min_length=1, max_length=250)
    x: int
    y: int
    metadata: Optional[ZoneMetadata] = None


class MaxLinkCapacity(BaseModel):
    max_link_capacity: Optional[int] = None


class ConnectionModel(BaseModel):
    name: str = Field(min_length=1, max_length=250)
    max_link_capacity: Optional[MaxLinkCapacity] = None
    

class Parser:
    def __init__(self, path):
        self.maps = []
        self.nb_drones = 0
        self.zones = []
        self.connections = []

        try:
            with open(path, 'r') as file:
                self.maps = file.readlines()

        except FileNotFoundError:
            raise ValueError(f'No such file: {path}')
        
        except PermissionError:
            raise ValueError(f'You have no permission access to: {path}')

        except Exception as e:
            raise ValueError(e)


    def extract_metadata(self, metadata):
        metadata = metadata[1:-1].split(' ')

        extracted = {}
        for pair in metadata:
            if '=' not in pair:
                raise ValueError('Invalid metadata!')

            key, value = pair.split('=')

            if key not in ['max_link_capacity', 'max_drones', 'color', 'zone']:
                raise ValueError(f'Invalid key: {key}')

            extracted[key] = int(value) if key in ['max_link_capacity', 'max_drones'] else value

        return extracted


    def print_zones(self):
        for z in self.zones:
            print(z)


    def print_connections(self):
        for c in self.connections:
            print(c)


    def parse(self):
        for line in self.maps:
            line = line.strip()
            if line.startswith('#') or line == '':
                continue


            try:
                key, value = line.split(':')
                key = key.strip()
                value = value.strip()
            except ValueError:
                raise ValueError('Invalid map structure!')

            if key == 'nb_drones':
                if self.nb_drones:
                    raise ValueError('Two entries for nb_drones')
                
                if self.zones or self.connections:
                    raise ValueError('The first line must be: nb_drones')

                try:
                    self.nb_drones = int(value)
                except ValueError:
                    raise ValueError('nb_drones must be a number!')


            elif key in ['start_hub', 'hub', 'end_hub']:

                if '[' not in value:
                    value += '[color=default]'

                bracket_index = value.index('[')

                name_and_coords = value[:bracket_index].strip().split(' ')
                metadata = value[bracket_index:].strip()

                if len(name_and_coords) != 3:
                    raise ValueError('Invalid zone structure!')

                try:
                    zone_name = name_and_coords[0]
                    zone_x = int(name_and_coords[1])
                    zone_y = int(name_and_coords[2])
                except ValueError:
                    raise ValueError('(X, Y) must be numbers!')


                self.zones.append({
                    'type': key,
                    'name': zone_name,
                    'x': zone_x,
                    'y': zone_y,
                    'metadata': self.extract_metadata(metadata),
                })


            elif key == 'connection':
                value = value.split(' ')
                if len(value) == 1:
                    value.append('[max_link_capacity=1]')

                try:
                    name, max_link_capacity = value
                except ValueError:
                    raise ValueError('Invalid connection structure!')

                self.connections.append({
                    'name': name,
                    'metadata': self.extract_metadata(max_link_capacity),
                })

            else:
                raise ValueError(f'Invalid key detected: {key}')


        if not self.nb_drones:
            raise ValueError('No nb_drones entry specified!')

        if not self.zones:
            raise ValueError('No zones entries specified!')

        if not self.connections:
            raise ValueError('No connections entries specified!')


    def get_map(self):
        return {
            'nb_drones': self.nb_drones,
            'zones': self.zones,
            'connections': self.connections,
        }


class Validate:
    def __init__(self, _map):
        self._map = _map
        self.validated_zones = []
        self.validated_connections = []

    def validate(self):
        nb_drones   = self._map['nb_drones']
        zones       = self._map['zones']
        connections = self._map['connections']

        for zone in zones:
            self.validated_zones.append(
                ZoneModel(**zone)
            )

        for connection in connections:
            self.validated_connections.append(
                ConnectionModel(**connection)
            )

        if not isinstance(nb_drones, int):
            raise ValueError('nb_drones must be an int!')

        if nb_drones <= 0:
            raise ValueError('nb_drones must be positive!')


class FlyInOrganizer:
    def __init__(self, zones, connections, nb_drones):
        self.zones       = []
        self.connections = []
        self.paths       = []
        self.start_zone  = None
        self.end_zone    = None
        self.drones      = [Drone() for _ in range(nb_drones)]


        # DEB
        # print(self.drones)
        # print()
        # for d in self.drones: print(d)
        # DEB


        for zone in zones:
            name        = zone['name']
            x           = zone['x']
            y           = zone['y']
            type        = zone['type']

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
                    type=type,
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
            if z.type == 'start_hub': self.start_zone = z
            if z.type == 'end_hub': self.end_zone = z



    def make_graph(self):
        Graph(self.connections, self.zones)


    def display_zones(self):
        for zone in self.zones:
            print(zone)


    @staticmethod
    def find_zone_by_name(zones, name):
        for zone in zones:
            if zone.name == name:
                return zone
        return None


    def find_path(self):
        visited = set()
        parent = {}

        queue = deque([self.start_zone])
        visited.add(self.start_zone)

        path = []

        while queue:
            neighbors = queue[0].neighbors

            for nbr in neighbors:
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append(nbr)
                    parent[nbr] = queue[0]

                    if nbr == self.end_zone:
                        current = nbr
                        while current != self.start_zone:
                            path.append(current)
                            current = parent[current]

                        path.append(self.start_zone)
                        return path[::-1]
                        
            queue.popleft()

        return None    



    def find_path(self):
        start = self.start_zone
        queue  = [start]
        visited = set()
        visited.add(start)

        path = []
        parent = {}

        while queue:
            current = queue[0]
            visited.add(current)

            neighbors = current.neighbors
            for nbr in neighbors:
                if nbr not in visited:
                    queue.append(nbr)
                    parent[nbr] = queue[0]
                    if nbr == self.end_zone:
                        while nbr != self.start_zone:
                            path.append(nbr)
                            nbr = parent[nbr]
                        path.append(start)
                        return path[::-1]

            queue.pop(0)
        return None



    def dijkstra_path_finder(self) -> list[Zone] | None:
        dist: dict[Zone, float] = {self.start_zone: 0}
        parent: dict[Zone, Zone] = {}

        counter = count()
        heap: list[tuple[float, int, Zone]] = [(0, next(counter), self.start_zone)]

        path: list[Zone] = []

        while heap:
            current_cost = heap[0][0]
            current_zone = heap[0][2]

            for nbr in current_zone.neighbors:
                new_cost = current_cost + nbr.move_cost

                if new_cost < dist.get(nbr, float('inf')):
                    dist[nbr] = new_cost
                    heapq.heappush(heap, (new_cost, next(counter), nbr))
                    parent[nbr] = current_zone

                    if nbr == self.end_zone:
                        current = nbr
                        while current != self.start_zone:
                            path.append(current)
                            current = parent[current]

                        path.append(self.start_zone)
                        return path[::-1]

            heapq.heappop(heap)

        return None


class Simulator:
    def __init__(self, flyin):
        self.flyin = flyin
        self.start_zone = flyin.start_zone
        self.end_zone = flyin.end_zone

        for drone in self.flyin.drones:
            self.start_zone.drones.append(drone)
            drone.zone = self.start_zone


        """ - each turn:
                - for each drone that hasn't reached goal:
                    - try to move to next zone in its path
                    - check zone capacity (max_drones)
                    - check connection capacity (max_link_capacity)
                    - if blocked → drone waits
                - print the turn output
                - repeat until all drones at goal
        """
        
        for drone in self.start_zone.drones:
            if drone.zone != self.end_zone:
                # SIMULATION LOGIC



def main():
    parser = Parser('maps/medium/03_priority_puzzle.txt')
    parser.parse()
    _map = parser.get_map()


    # DEB
    # parser.print_zones()
    # DEB


    # try:
    #     parser = Parser('maps/medium/03_priority_puzzle.txt')
    #     parser.parse()
    # except ValueError as e:
    #     print(e)


    try:
        validator = Validate(_map)
        validator.validate()
    except ValidationError as e:
        print(f"Pydantic error: {e.errors()[0]['msg']}")


    flyin = FlyInOrganizer(parser.zones, parser.connections, parser.nb_drones)
    flyin.make_graph()

    # # DEB
    # for zone in flyin.zones: print(zone)
    # # DEB


    path = flyin.dijkstra_path_finder()


    simulation = Simulator(flyin)


    # # DEB
    # print('\nPATH: ', end='')
    # if path:
    #     print(' -> '.join([z.name for z in path]))



if __name__ == "__main__":
    main()

