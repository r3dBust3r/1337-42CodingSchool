from pydantic import BaseModel, Field


class LevelConfig(BaseModel):
    width: int = Field(default=28)
    height: int = Field(default=31)


class ConfigModel(BaseModel):
    highscore_filename: str = Field(default="highscores.json")
    level: list[LevelConfig] = Field(default_factory=lambda: [LevelConfig()])
    lives: int = Field(default=3)
    pacgum: int = Field(default=42)
    points_per_pacgum: int = Field(default=10)
    points_per_super_pacgum: int = Field(default=50)
    points_per_ghost: int = Field(default=200)
    seed: int = Field(default=42)
    level_max_time: int = Field(default=90)
