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
