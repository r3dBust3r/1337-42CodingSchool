class Connection:
    def __init__(self, name, max_link_capacity=1):
        self.name = name
        self.max_link_capacity = max_link_capacity
        self.current_drones = []

    def __str__(self):
        return f"{self.name} ({self.max_link_capacity})"
