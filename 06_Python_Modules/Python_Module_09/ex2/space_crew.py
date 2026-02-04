from pydantic import BaseModel  # type: ignore
from pydantic import Field  # type: ignore
from pydantic import ValidationError  # type: ignore
from pydantic import model_validator  # type: ignore

from typing import List, Dict
from datetime import datetime
from enum import Enum


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_rules(self) -> 'SpaceMission':

        if not self.mission_id.startswith('M'):
            raise ValueError('Mission ID must start with "M"')

        captain: bool = False
        for member in self.crew:
            if (
                member.rank == member.rank.CAPTAIN or
                member.rank == member.rank.COMMANDER
            ):
                captain = True

        if not captain:
            raise ValueError(
                'Mission must have at least one Commander or Captain'
            )

        if self.duration_days > 365:
            experienced_member_count: int = 0
            for member in self.crew:
                if member.years_experience >= 5:
                    experienced_member_count += 1

            if experienced_member_count < len(self.crew) / 2:
                raise ValueError(
                    'Long missions (> 365 days) '
                    'need 50% experienced crew (5+ years)'
                )

        for member in self.crew:
            if not member.is_active:
                raise ValueError('All crew members must be active')

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 40)

    try:
        crew: List[CrewMember] = []
        members: Dict[str, List] = {
            'Sarah Connor': [Rank.COMMANDER, 58, "something", 28],
            'John Smith': [Rank.LIEUTENANT, 53, "something", 13],
            'Alice Johnson': [Rank.OFFICER, 47, "something", 19],
            'James keneddy': [Rank.OFFICER, 45, "something", 12],
            'Leon Scott': [Rank.CADET, 23, "something", 0],
            'Jack Kraouser': [Rank.CADET, 28, "something", 3],
            'Tommas Brown': [Rank.CADET, 29, "something", 7],
            'Edward Martiniz': [Rank.CADET, 31, "something", 9],
        }
        id: int = 0
        for name, info in members.items():
            crw: CrewMember = CrewMember(
                member_id=f"CM_00{110+id}",
                name=name,
                rank=info[0],
                age=info[1],
                specialization=info[2],
                years_experience=info[3],
                is_active=True
            )
            id += 1
            crew.append(crw)

        mission: SpaceMission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2028, 10, 1),
            duration_days=900,
            crew=crew[:3],
            budget_millions=2500.0
        )

        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")
        print("Crew members:")
        for c in mission.crew:
            print(f" - {c.name} ({c.rank}) - ", end="")
            if c.rank == 'commander':
                print('Mission Command')
            elif c.rank == 'lieutenant':
                print('Navigation')
            elif c.rank == 'officer':
                print('Engineering')
            else:
                print('Unknown')

        print()
        print("=" * 40)
        print("Expected validation error:")

        SpaceMission(
            mission_id="M2025_MOON",
            mission_name="Moon Colony Establishment",
            destination="Moon",
            launch_date=datetime(2026, 10, 1),
            duration_days=100,
            crew=crew[len(crew)-4:len(crew)-1],
            budget_millions=90.5
        )

    except ValidationError as e:
        print(e.errors()[0]['msg'].replace('Value error, ', ''))


if __name__ == "__main__":
    main()
