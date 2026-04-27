class Graph:

    @staticmethod
    def find_zone_by_name(zones, name):
        for zone in zones:
            if zone.name == name:
                return zone
        return None


    def __init__(self, connections, zones):

        for conn in connections:
            if '-' not in conn.name:
                raise ValueError('Invalid connection name!')

            start, end = conn.name.split('-')

            start = self.find_zone_by_name(zones, start)
            end   = self.find_zone_by_name(zones, end)

            if not start or not end:
                raise ValueError(f'Invalid connection between ({start} <-> {end})')

            start.add_neighbor(end)
            end.add_neighbor(start)
