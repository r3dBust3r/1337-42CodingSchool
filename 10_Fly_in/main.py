from pydantic import BaseModel, ValidationError, Field
from typing import Literal, Dict, Optional
from zone import Zone
from connection import Connection
from graph import Graph
from collections import deque


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
    def __init__(self, zones, connections):
        self.zones       = []
        self.connections = []
        self.paths       = []
        self.start_zone  = None
        self.end_zone    = None


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
                    queue.append(nbr)
                    parent[nbr] = queue[0]
                    visited.add(nbr)

                    if nbr == self.end_zone:
                        current = nbr
                        while current != self.start_zone:
                            path.append(current)
                            current = parent[current]

                        path.append(self.start_zone)
                        return path[::-1]
                        
            queue.popleft()

        return None



def main():
    parser = Parser('maps/hard/02_capacity_hell.txt')
    parser.parse()
    _map = parser.get_map()


    # DEB
    parser.print_zones()
    # DEB


    # try:
    #     parser = Parser('maps/hard/02_capacity_hell.txt')
    #     parser.parse()
    # except ValueError as e:
    #     print(e)


    try:
        validator = Validate(_map)
        validator.validate()
    except ValidationError as e:
        print(f"Pydantic error: {e.errors()[0]['msg']}")


    flyin = FlyInOrganizer(parser.zones, parser.connections)
    flyin.make_graph()
    for zone in flyin.zones:
        print(zone)


    path = flyin.find_path()


    # DEB
    print('\nPATH: ', end='')
    if path:
        print(' -> '.join([z.name for z in path]))



if __name__ == "__main__":
    main()
