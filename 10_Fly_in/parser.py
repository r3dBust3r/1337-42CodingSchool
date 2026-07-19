from typing import List, Dict, Any


class Parser:
    """Parse and validate a Fly-in map file into structured data."""

    def __init__(self, path: str) -> None:
        """Load the raw map file from disk.

        Args:
            path: Path to the map file.
        """
        self.__map: List[str] = []
        self.nb_drones: int = 0
        self.zones: List[Dict[str, Any]] = []
        self.connections: List[Dict[str, Any]] = []
        self.start_zone: str = ''
        self.end_zone: str = ''

        try:
            with open(path, 'r') as file:
                self.__map = file.readlines()

        except FileNotFoundError:
            raise ValueError(f'> No such file: {path}')

        except PermissionError:
            raise ValueError(f'> You have no permission access to: {path}')

        except Exception as e:
            raise ValueError(e)

    def extract_metadata(
            self,
            raw_metadata: str,
            zone_type: str,
            line_nbr: str,
            zone: bool
    ) -> Dict:
        """Parse a metadata block into a dictionary."""
        if raw_metadata.count('[') != 1 or raw_metadata.count(']') != 1:
            raise ValueError(
                f'{line_nbr}Invalid metadata format!\n'
                'Valid format: [key1=value1 key2=value2]'
            )
        metadata = raw_metadata[1:-1].split(' ')

        extracted = {}
        for pair in metadata:
            if not pair:
                continue

            if pair.count('=') != 1:
                raise ValueError(
                    f'{line_nbr}Invalid metadata format!\n'
                    'Valid format: [key1=value1 key2=value2]'
                )

            value: str | int
            key, value = pair.split('=')

            if key in extracted:
                raise ValueError(f'{line_nbr}Duplicated metadata key: {key}')

            if zone and key not in ['max_drones', 'color', 'zone']:
                raise ValueError(
                    f'{line_nbr}Invalid metadata key ({key}) for a zone'
                )

            elif not zone and key != 'max_link_capacity':
                raise ValueError(
                    f'{line_nbr}Invalid metadata key ({key}) for a connection'
                )

            if key == 'color':
                if not value.isalpha():
                    raise ValueError(f'{line_nbr}Color must be one valid word')

            if key == 'zone' and value not in [
                'normal',
                'blocked',
                'restricted',
                'priority'
            ]:
                raise ValueError(
                    f'{line_nbr}Zone type must be one of: '
                    'normal, blocked, restricted or priority'
                )

            if key in ['max_link_capacity', 'max_drones']:
                try:
                    value = int(value)
                except ValueError:
                    raise ValueError(
                        f'{line_nbr}max_link_capacity & max_drones '
                        'must be valid numbers'
                    )

                if zone_type in ['start_hub', 'end_hub']:
                    value = self.nb_drones
                else:
                    if value < 1:
                        raise ValueError(
                            f'{line_nbr}max_link_capacity & max_drones '
                            'must be strictly positive numbers'
                        )

            extracted[key] = value

        return extracted

    def parse(self) -> None:
        """Validate and convert the raw map lines into parser state."""
        line_nbr: int | str

        for line_nbr, line in enumerate(self.__map):
            line_nbr = f'Error in line: {line_nbr + 1}\n> '
            line = line.strip().lower()

            # full line comments
            if line.startswith('#') or line == '':
                continue

            # inline comments
            if '#' in line:
                line = line[:line.find('#')]

            # a line with no key: value
            try:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
            except ValueError:
                raise ValueError(f'{line_nbr}Invalid map structure!')

            if key == 'nb_drones':
                # number of drones might be:
                # duplicated
                # not the first line
                # not a number
                # negative

                if self.nb_drones:
                    raise ValueError(f'{line_nbr}Two entries for nb_drones')

                if self.zones or self.connections:
                    raise ValueError(
                        f'{line_nbr}The first line must be: nb_drones'
                    )

                try:
                    self.nb_drones = int(value)
                except ValueError:
                    raise ValueError(
                        f'{line_nbr}nb_drones must be a valid number!'
                    )

                if self.nb_drones < 1:
                    raise ValueError(
                        f'{line_nbr}nb_drones must be strictly positive!'
                    )

            elif key in ['start_hub', 'hub', 'end_hub']:
                # checking if metadata was presented
                # if not: add the defalut values
                if '[' not in value:
                    value += '[zone=normal color=default max_drones=1]'

                bracket_index = value.index('[')

                name_and_coords = value[:bracket_index].strip().split(' ')
                metadata = value[bracket_index:].strip()

                name_and_coords = [a for a in name_and_coords if a]

                if len(name_and_coords) != 3:
                    raise ValueError(
                        f'{line_nbr}Invalid zone structure!\n'
                        'Valid format: <name> <x> <y> [<metadata>]'
                    )

                try:
                    zone_x: str | int
                    zone_y: str | int

                    zone_name, zone_x, zone_y = name_and_coords

                    zone_x = int(zone_x)
                    zone_y = int(zone_y)

                except ValueError:
                    raise ValueError(
                        f'{line_nbr}coordinates (x, y) '
                        f'must be valid integers!'
                    )

                if zone_name in [z['name'] for z in self.zones]:
                    raise ValueError(
                        f'{line_nbr}Found a duplicated zone: {zone_name}'
                    )

                if (zone_x, zone_y) in [(z['x'], z['y']) for z in self.zones]:
                    raise ValueError(
                        f'{line_nbr}Found duplicated coodrinates: '
                        f'{(zone_x, zone_y)}'
                    )

                if key == 'start_hub' and self.start_zone:
                    raise ValueError(f'{line_nbr}start_zone is duplicated!')

                if key == 'end_hub' and self.end_zone:
                    raise ValueError(f'{line_nbr}end_zone is duplicated!')

                if key == 'start_hub':
                    self.start_zone = zone_name

                if key == 'end_hub':
                    self.end_zone = zone_name

                # invalid zone name
                if '-' in zone_name or ']' in zone_name:
                    raise ValueError(
                        f'{line_nbr}Name cannot contain a '
                        'HASH, DASH, SPACE or BRACKETS'
                    )

                # all checks passed
                self.zones.append({
                    'hub_type': key,
                    'name': zone_name,
                    'x': zone_x,
                    'y': zone_y,
                    'metadata': self.extract_metadata(
                        metadata,
                        key,
                        line_nbr,
                        True
                    )
                })

            elif key == 'connection':
                splt_value = value.split(' ', 1)
                splt_value = [a for a in splt_value if a]

                # no metadata: add the default
                if len(splt_value) == 1:
                    splt_value.append('[max_link_capacity=1]')

                try:
                    name, max_link_capacity = splt_value
                    max_link_capacity = max_link_capacity.strip()
                except ValueError:
                    raise ValueError(
                        f'{line_nbr}Invalid connection structure!\n'
                        'Valid format: <zone1>-<zone2> [<metadata>]'
                    )

                # invalid conn name
                if name.count('-') != 1:
                    raise ValueError(
                        f'{line_nbr}Invalid connection name\n'
                        'Valid format: <zone1>-<zone2>'
                    )

                z1_name, z2_name = name.split('-')

                if z1_name == z2_name:
                    raise ValueError(
                        f'{line_nbr}{z1_name} self connection'
                    )

                if z1_name not in [z['name'] for z in self.zones]:
                    raise ValueError(
                        f'{line_nbr}{z1_name} zone does not exist'
                    )

                if z2_name not in [z['name'] for z in self.zones]:
                    raise ValueError(
                        f'{line_nbr}{z2_name} zone does not exist'
                    )

                # conn is duplicated
                con_names = [c['name'] for c in self.connections]
                if name in con_names or f'{z2_name}-{z1_name}' in con_names:
                    raise ValueError(
                        f'{line_nbr}Found a duplicated connection: {name}'
                    )

                # conn checks passed
                self.connections.append({
                    'name': name,
                    'metadata': self.extract_metadata(
                        max_link_capacity,
                        '',
                        line_nbr,
                        False
                    ),
                })

            else:
                raise ValueError(f'{line_nbr}Invalid key detected: {key}')

        if not self.nb_drones:
            raise ValueError('> No nb_drones entry specified!')

        if not self.zones:
            raise ValueError('> No zones entries specified!')

        if not self.connections:
            raise ValueError('> No connections entries specified!')

        if not self.start_zone:
            raise ValueError('> No start zone specified!')

        if not self.end_zone:
            raise ValueError('> No end zone specified!')

    def get_map(self) -> Dict[str, Any]:
        """Return the parsed map structure."""
        return {
            'nb_drones': self.nb_drones,
            'zones': self.zones,
            'connections': self.connections,
        }
