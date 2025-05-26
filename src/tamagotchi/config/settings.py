from dataclasses import dataclass, field
from typing import Dict, Tuple

@dataclass
class GameSettings:
    """Game-specific settings."""
    TITLE: str = "Tamagotchi"
    WINDOW_WIDTH: int = 400
    WINDOW_HEIGHT: int = 600
    FPS: int = 60
    WHITE: str = "#FFFFFF"
    BLACK: str = "#000000"
    GRAY: str = "#C8C8C8"
    DARK_GRAY: str = "#646464"
    RED: str = "#FF0000"
    YELLOW: str = "#FFFF00"
    GREEN: str = "#00FF00"

@dataclass
class PetSettings:
    """Pet-specific settings."""
    HUNGER_RATE: float = 0.5
    HAPPINESS_RATE: float = 0.3
    ENERGY_RATE: float = 0.4
    SLEEP_ENERGY_RECOVERY: float = 5.0
    FEED_HUNGER_RECOVERY: float = 30.0
    PLAY_HAPPINESS_RECOVERY: float = 25.0
    PLAY_ENERGY_COST: float = 15.0

@dataclass
class UISettings:
    """UI-specific settings."""
    FONT_SIZE_LARGE: int = 24
    FONT_SIZE_SMALL: int = 16
    BUTTON_WIDTH: int = 100
    BUTTON_HEIGHT: int = 40
    BAR_WIDTH: int = 200
    BAR_HEIGHT: int = 20
    INPUT_WIDTH: int = 200
    INPUT_HEIGHT: int = 40

@dataclass
class Settings:
    """Main settings container."""
    game: GameSettings = field(default_factory=GameSettings)
    pet: PetSettings = field(default_factory=PetSettings)
    ui: UISettings = field(default_factory=UISettings)

# Create global settings instance
settings = Settings() 