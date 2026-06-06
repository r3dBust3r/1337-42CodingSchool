from pydantic import BaseModel, ValidationError, Field  # type: ignore
from typing import Literal, Dict, Optional
from zone import Zone
from connection import Connection
from drone import Drone
from collections import deque
from itertools import count
import heapq



class ZoneMetadata(BaseModel):
    color: Optional[str] = None
    max_drones: Optional[int] = None
    zone: Literal['normal', 'blocked', 'restricted', 'priority'] = 'normal'


class ZoneModel(BaseModel):
    hub_type: Literal['start_hub', 'hub', 'end_hub']
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
                    'hub_type': key,
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


class Validator:
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


    def bfs_fastest_path(self):
        queue   = deque()
        visited = set()
        parent  = dict()

        queue.append(self.start_zone)
        visited.add(self.start_zone)
        parent[self.start_zone] = None

        path = []

        while queue:
            current = queue[0]

            neighbors = current.neighbors

            for neighbor in neighbors:
                if neighbor in visited:
                    continue

                if neighbor.zone == 'blocked':
                    continue

                parent[neighbor] = current

                visited.add(neighbor)
                queue.append(neighbor)

                if neighbor == self.end_zone:
                    current = neighbor
                    while current:
                        path.append(current)
                        current = parent[current]

                    return path[::-1]

            queue.popleft()

        return None


    def dijkstra_fastest_path(self, remaining_capacity):
        heap = []
        counter = count()

        visited = set()
        parent = {self.start_zone: None}
        dist = {self.start_zone: 0}

        heapq.heappush(heap, (0, next(counter), self.start_zone))

        while heap:
            current_cost, _, current = heapq.heappop(heap)

            if current in visited:
                continue

            visited.add(current)

            if current == self.end_zone:
                path = []
                while current:
                    path.append(current)
                    current = parent[current]
                return path[::-1]

            for neighbor in current.neighbors:

                if neighbor.zone == 'blocked':
                    continue

                if neighbor != self.end_zone:
                    if remaining_capacity.get(neighbor, 0) <= 0:
                        continue

                new_cost = current_cost + neighbor.move_cost

                if neighbor not in dist or new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    parent[neighbor] = current
                    heapq.heappush(heap, (new_cost, next(counter), neighbor))

        return None


    def find_multiple_paths(self):
        remaining_capacity = {z: z.max_drones for z in self.zones}

        for d in self.drones:
            path = self.dijkstra_fastest_path(remaining_capacity)
            if path:
                d.path = path
                for z in path:
                    if z in [self.start_zone, self.end_zone]:
                        continue

                    remaining_capacity[z] -= 1



def main():
    try:
        parser = Parser('maps/medium/03_priority_puzzle.txt')
        parser.parse()
        _map = parser.get_map()
    except ValueError as e:
        print(e)
        exit(1)

    try:
        validator = Validator(_map)
        validator.validate()
    except ValidationError as e:
        print(f"Pydantic error: {e.errors()[0]['msg']}")
        exit(1)


    graph = Graph(
        parser.zones,
        parser.connections,
        parser.nb_drones
    )

    try: graph.create_graph()
    except ValueError as e:
        print(e)
        exit(1)


    # fastest_path = graph.dijkstra_fastest_path()
    # print(' -> '.join( [z.name for z in fastest_path] ))

    graph.find_multiple_paths()

    for d in graph.drones:
        print(f'{d.id}: {" -> ".join([z.name for z in d.path])}')

    # ---

    # for z in graph.zones: print(z)
    # print()

    # for c in graph.connections: print(c)
    # print()

    # print(graph.start_zone)
    # print(graph.end_zone)

    # print()
    # for d in graph.drones:
    #     print(
    #         f'Drone ({d.id}) in: {d.current_zone.name},'
    #         f' destination: {d.end_zone.name}, deliverd: {d.delivered}'
    #     )
    # print()

    # for z in graph.zones: print(f'zone: {z.name} has ({", ".join([n.name for n in z.neighbors])}) neighbors')

    # ---


if __name__ == "__main__":
    main()
