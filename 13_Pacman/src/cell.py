from typing import Any

class Cell:
    def __init__(self, walls: int, has_pacgum: bool = False, super_pacgum: bool = False) -> None:
        self.walls = walls
        self.has_pacgum = has_pacgum
        self.super_pacgum = super_pacgum
        self.fruit: Any = None

