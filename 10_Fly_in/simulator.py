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


            self.turns.append(turns.strip())



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
