class Drone:
    d_id = 1
    def __init__(self, end_zone):
        self.id = f'D{Drone.d_id}'
        self.current_zone = None
        self.path = []
        self.path_index = 0
        self.end_zone = end_zone

        Drone.d_id += 1

    @property
    def delivered(self):
        return self.current_zone == self.end_zone
