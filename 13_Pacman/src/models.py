from pydantic import BaseModel, Field


class LevelConfig(BaseModel):
    width: int = Field(default=15, ge=2, le=42)
    height: int = Field(default=9, ge=2, le=42)


class ConfigModel(BaseModel):
    highscore_filename: str = Field(default="highscores.json")
    level: list[LevelConfig] = Field(
        default_factory=lambda: [LevelConfig()],
        min_length=1,
        max_length=999
    )
    lives: int = Field(default=3, ge=1, le=999)
    pacgum: int = Field(default=42, ge=0)
    points_per_pacgum: int = Field(default=10, ge=0, le=9999)
    points_per_super_pacgum: int = Field(default=50, ge=0, le=9999)
    points_per_ghost: int = Field(default=200, ge=0, le=9999)
    seed: int = Field(default=42)
    level_max_time: int = Field(default=90, ge=5, le=9999)
