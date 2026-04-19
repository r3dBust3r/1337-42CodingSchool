"""
    - [+] read file as lines
    - [+] loop trought them
    - [+] strip them
    - [+] ignore comments #
    - [+] split by (:)
    - [+] if line starts with nb_drones, store them and continue
    - [+] if line starts with start_hub, end_hub, hub, start extracting zones
        - [+] split by space ( )
            - [+] name      -> [0]
            - [+] x         -> [1]
            - [+] y         -> [2]
            - [+] metadata  -> [3]
                - [+] remove [  and  ]
                - [+] split by: (=)
                    if key in color, zone, max_drones
                        - [+] {key[0]: value[1]}

    - [+] if line starts with connection, start extracting connections
        - [+] splie by space: ( )
        - [+] name              --> [0] 
        - [+] max_link_capacity --> [1]
            - [+] remove ([) and (])
            - [+] split by: (=) 
            - [+] grab [1]
            - [+] convert into intg
"""


class Parser:
    def __init__(self, path):
        self._map = []
        self._nb_drones = 0
        self._zones = []
        self._connections = []

        try:
            with open(path, 'rt') as file:
                self._map = file.readlines()
        except FileNotFoundError:
            print(f'No fuch file: {path}')
        except PermissionError:
            print(f'No access permission for: {path}')
        except Exception as e:
            print(e)

        for line in self._map:
            line = line.strip()
            if line.startswith('#') or line == '':
                continue
            
            line = line.split(':')
            if len(line) != 2:
                raise ValueError('Invalid map file!')
            
            key, value = line

            key = key.strip().lower()
            value = value.strip().lower()

            name     = ''
            hub_x    = 0
            hub_y    = 0
            metadata = {}


            if key == 'nb_drones':
                try:
                    self._nb_drones = int(value)
                except Exception as e:
                    print(e)

            elif key in ['start_hub', 'end_hub', 'hub']:
                value = value.split(' ')
                if len(value) < 3:
                    raise ValueError('Invalid hub metadata!')

                name     = value[0]
                hub_x    = int(value[1])
                hub_y    = int(value[2])
                metadata = '[zone=normal]'

                if len(value) > 3:
                    metadata = ' '.join(value[3:])

                metadata = self.parse_metadata(metadata)

                if not metadata:
                    raise ValueError('Invalid metadata structure!')

                self._zones.append({
                    'name': name,
                    'hub_x': hub_x,
                    'hub_y': hub_y,
                    'metadata': metadata,
                })

            elif key == 'connection':
                value = value.split(' ')
                if len(value) not in [1, 2]:
                    raise ValueError('Invalid connection!')
                
                name     = value[0]
                metadata = '[max_link_capacity=1]'

                metadata = self.parse_metadata(metadata)

                if not metadata:
                    raise ValueError('Invalid metadata structure!')

                if len(value) == 2:
                   metadata = value[1]

                self._connections.append({
                    'name': name,
                    'metadata': metadata,
                })
        ...


    def extract_map_data(self):
        return {
            'nb_drones': self._nb_drones,
            'zones': self._zones,
            'connections': self._connections
        }
        ...


    @staticmethod
    def parse_metadata(metadata):
        if not metadata.startswith('[') or not metadata.endswith(']'):
            return None

        parsed_metadata = {}
        keys = ['color', 'max_drones', 'max_link_capacity', 'zone']
        zones = ['priority', 'normal', 'restricted', 'blocked']

        try:
            values = metadata[1:-1].strip().split(' ')
            for val in values:
                key, value = val.split('=')
                if key not in keys:
                    raise ValueError('Invalid key detected!')
                
                if key == 'zone' and value not in zones:
                    raise ValueError('Invalid zone type detected!')

                parsed_metadata[key] = int(value) if key in ['max_drones', 'max_link_capacity'] else value
        except Exception as e:
            print(e)
            return None

        return parsed_metadata
        ...
    ...


def main():
    try:
        parser = Parser("maps/easy/01_linear_path.txt")
    except Exception as e:
        print(e)
        exit(1)

    map = parser.extract_map_data()

    for k, v in map.items():
        print(f'[ {k} ]')

        if isinstance(v, list):
            for item in v: print(item)
        else: print(v)

        print('-' * 42)
        print()
    ...


if __name__ == "__main__":
    main()
    ...
