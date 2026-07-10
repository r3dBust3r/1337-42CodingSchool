from pydantic import BaseModel, ValidationError, Field  # type: ignore
from typing import Literal, Dict, Optional
from zone import Zone
from connection import Connection
from drone import Drone
from collections import deque
from itertools import count
import heapq
from sys import argv
import arcade # type: ignore



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


class Simulator:
    def __init__(self, graph, paths):
        self.graph = graph
        self.paths = paths
        self.using_conns = {}
        self.turns = []

        self.assign_paths_to_drones()
        self.init_conns()


    def assign_paths_to_drones(self):
        for d in self.graph.drones:
            d_id = int(d.id.replace('D', ''))
            d.path = self.paths[d_id % len(self.paths)]


    def init_conns(self):
        for conn in self.graph.connections:
            self.using_conns[conn.name] = 0


    def run(self):
        while not self._all_delivered():
            turns = ''

            for d in self.graph.drones:

                if d.delivered:
                    continue

                cur_zone = d.path[1][d.path_index]
                nxt_zone = d.path[1][d.path_index + 1]

                conn = self._get_conn(cur_zone, nxt_zone)

                if nxt_zone.zone in ['normal', 'priority']:

                    # next zone has no space
                    if len(nxt_zone.current_drones) == nxt_zone.max_drones:
                        continue

                    # connection has no space
                    if self.using_conns[conn.name] == conn.current_drones:
                        continue

                    self._move_drone(d, cur_zone, nxt_zone)
                    turns += f'{d.id}-{nxt_zone.name} '

                elif nxt_zone.zone == 'restricted':
                    if d.in_transit:
                        self._move_drone(d, cur_zone, nxt_zone)
                        turns += f'{d.id}-{nxt_zone.name} '
                        d.in_transit = False

                        self.using_conns[conn.name] -= 1

                    else:
                        if len(nxt_zone.current_drones) == nxt_zone.max_drones:
                            continue

                        if self.using_conns[conn.name] == conn.current_drones:
                            continue

                        self._move_drone(d, cur_zone, conn, False)
                        d.in_transit = True

                        self.using_conns[conn.name] += 1

                        turns += f'{d.id}-{conn.name} '


            self.turns.append(turns)



    def _all_delivered(self):
        return len(self.graph.drones) == len(self.graph.end_zone.current_drones)


    def _move_drone(self, d, cur, nxt, to_zone=True):
        if to_zone:
            d.path_index += 1

        d.current_zone = nxt

        if d in cur.current_drones: cur.current_drones.remove(d)
        nxt.current_drones.append(d)


    def _get_conn(self, z1, z2):
        for conn in self.graph.connections:
            if conn.name == f'{z1.name}-{z2.name}' or conn.name == f'{z2.name}-{z1.name}':
                return conn
        return None


    def display_turns(self):
        for t in self.turns:
            print(t)

        print(f'\nTotal turns: {len(self.turns)}')


class Visualizer(arcade.View):
    def __init__(self, graph, turns):
        self.graph = graph
        self.turns = turns
        self.scale = 300
        self.zone_size = 25

        super().__init__()
        self.background_color = arcade.color.BURLYWOOD


    def on_draw(self):
        self.clear()

        # Drawing Connections
        for conn in self.graph.connections:
            z1, z2 = conn.name.split('-')

            z1 = self._get_zone(z1)
            z2 = self._get_zone(z2)

            z1_x = z1.x * self.scale + self.zone_size * 2
            z1_y = z1.y * self.scale - self.zone_size * 2

            z2_x = z2.x * self.scale + self.zone_size * 2
            z2_y = z2.y * self.scale - self.zone_size * 2

            arcade.draw_line(
                z1_x + self.zone_size,
                z1_y + 960 - self.zone_size,
                z2_x + self.zone_size,
                z2_y + 960 - self.zone_size,
                arcade.color.BLACK,
                4
            )

        # Drawing Zones
        for z in self.graph.zones:
            x = z.x * self.scale + self.zone_size * 2
            y = z.y * self.scale - self.zone_size * 2

            arcade.draw_circle_filled(
                x + self.zone_size,
                y + 960 - self.zone_size,
                self.zone_size,
                arcade.color.BLACK
            )

            arcade.draw_text(
                    z.name.upper(),
                    x + self.zone_size - len(z.name) * 5,
                    y + 960 - self.zone_size * 2.8,
                    arcade.color.BLACK,
                    12
            )


    def on_update(self, delta_time):
        self.delta_time = delta_time


    def _get_zone(self, name):
        for zone in self.graph.zones:
            if zone.name == name:
                return zone
        return None



def main():
    try:
        parser = Parser(argv[1])
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


    paths = graph.find_multiple_paths()
    simulator = Simulator(graph, paths)
    simulator.run()
    # simulator.display_turns()


    window = arcade.Window(1920, 960, "Fly-in Simulation")
    visualizer = Visualizer(graph, simulator.turns)
    window.show_view(visualizer)
    arcade.run()


    # for p in paths:
    #     c, p = p
    #     print(c, end=": ")
    #     print(' -> '.join([z.name for z in p]))


if __name__ == "__main__":
    main()
