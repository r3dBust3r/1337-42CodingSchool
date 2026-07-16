from typing import List, Dict, Any


class Parser:
    def __init__(self, path: str) -> None:
        self.maps: List[str] = []
        self.nb_drones: int = 0
        self.zones: List[Dict[str, Any]] = []
        self.connections: List[Dict[str, Any]] = []

        try:
            with open(path, 'r') as file:
                self.maps = file.readlines()

        except FileNotFoundError:
            raise ValueError(f'No such file: {path}')

        except PermissionError:
            raise ValueError(f'You have no permission access to: {path}')

        except Exception as e:
            raise ValueError(e)

    def extract_metadata(self, raw_metadata: str) -> Dict:
        metadata = raw_metadata[1:-1].split(' ')

        extracted = {}
        for pair in metadata:
            if '=' not in pair:
                raise ValueError('Invalid metadata!')

            key, value = pair.split('=')

            if key not in [
                'max_link_capacity',
                'max_drones',
                'color',
                'zone'
            ]:
                raise ValueError(f'Invalid key: {key}')

            extracted[key] = int(value) if key in \
                ['max_link_capacity', 'max_drones'] else value

        return extracted

    def parse(self) -> None:
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
                splt_value = value.split(' ')
                if len(splt_value) == 1:
                    splt_value.append('[max_link_capacity=1]')

                try:
                    name, max_link_capacity = splt_value
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

    def get_map(self) -> Dict[str, Any]:
        return {
            'nb_drones': self.nb_drones,
            'zones': self.zones,
            'connections': self.connections,
        }
