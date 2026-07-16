from pydantic import BaseModel, Field
from typing import Literal, Optional
from typing import List, Dict, Any


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


class Validator:
    def __init__(self, _map: Dict[str, Any]) -> None:
        self._map = _map
        self.validated_zones: List[ZoneModel] = []
        self.validated_connections: List[ConnectionModel] = []

    def validate(self) -> None:
        nb_drones = self._map['nb_drones']
        zones = self._map['zones']
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
