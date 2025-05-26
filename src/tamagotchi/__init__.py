"""A modern Tamagotchi-style virtual pet game."""

__version__ = "1.0.0"

from .core.pet import Tamagotchi
from .ui.game import Game

__all__ = ["Tamagotchi", "Game"] 