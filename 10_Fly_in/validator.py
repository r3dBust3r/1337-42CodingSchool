from pydantic import BaseModel, Field
from typing import Literal, Optional
from typing import List, Dict, Any


class ZoneMetadata(BaseModel):
    """Pydantic model for zone metadata."""

    color: Optional[str] = None
    max_drones: Optional[int] = None
    zone: Literal['normal', 'blocked', 'restricted', 'priority'] = 'normal'


class ZoneModel(BaseModel):
    """Pydantic model for a parsed zone."""

    hub_type: Literal['start_hub', 'hub', 'end_hub']
    name: str = Field(min_length=1, max_length=250)
    x: int
    y: int
    metadata: Optional[ZoneMetadata] = None


class MaxLinkCapacity(BaseModel):
    """Pydantic model for connection capacity metadata."""

    max_link_capacity: Optional[int] = None


class ConnectionModel(BaseModel):
    """Pydantic model for a parsed connection."""

    name: str = Field(min_length=1, max_length=250)
    max_link_capacity: Optional[MaxLinkCapacity] = None


class Validator:
    """Validate the parsed map using Pydantic models."""

    def __init__(self, _map: Dict[str, Any]) -> None:
        """Store the parsed map and prepare validation results."""
        self._map = _map
        self.validated_zones: List[ZoneModel] = []
        self.validated_connections: List[ConnectionModel] = []

    def validate(self) -> None:
        """Validate zones, connections, and drone count."""
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
