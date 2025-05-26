from dataclasses import dataclass, field
from typing import Optional
import time
from ..config.settings import settings

@dataclass
class Tamagotchi:
    """A virtual pet with various needs and states."""
    name: str
    hunger: float = field(default=100.0)  # Max stat is 100
    happiness: float = field(default=100.0)  # Max stat is 100
    energy: float = field(default=100.0)  # Max stat is 100
    last_update: float = field(default_factory=time.time)
    age: int = field(default=0)
    is_sleeping: bool = field(default=False)
    is_alive: bool = field(default=True)

    def update(self) -> None:
        """Update pet stats based on time passed."""
        current_time = time.time()
        time_passed = current_time - self.last_update
        
        # Decrease stats over time
        self.hunger = max(
            0.0,  # Min stat is 0
            self.hunger - time_passed * settings.pet.HUNGER_RATE
        )
        self.happiness = max(
            0.0,  # Min stat is 0
            self.happiness - time_passed * settings.pet.HAPPINESS_RATE
        )
        if self.is_sleeping:
            self.energy = min(
                100.0,
                self.energy + time_passed * settings.pet.SLEEP_ENERGY_RECOVERY
            )
            # Wake up automatically if energy is full
            if self.energy >= 100.0:
                self.energy = 100.0
                self.is_sleeping = False
        else:
            self.energy = max(
                0.0,  # Min stat is 0
                self.energy - time_passed * settings.pet.ENERGY_RATE
            )
        
        # Check if pet is still alive
        if self.hunger <= 0.0 or self.happiness <= 0.0:
            self.is_alive = False
        
        self.last_update = current_time

    def feed(self) -> None:
        """Feed the pet to increase hunger."""
        if self.is_alive and not self.is_sleeping:
            self.hunger = min(
                100.0,  # Max stat is 100
                self.hunger + settings.pet.FEED_HUNGER_RECOVERY
            )

    def play(self) -> None:
        """Play with the pet to increase happiness but decrease energy."""
        if self.is_alive and not self.is_sleeping:
            self.happiness = min(
                100.0,  # Max stat is 100
                self.happiness + settings.pet.PLAY_HAPPINESS_RECOVERY
            )
            self.energy = max(
                0.0,  # Min stat is 0
                self.energy - settings.pet.PLAY_ENERGY_COST
            )

    def sleep(self) -> None:
        """Toggle sleep mode and restore energy when sleeping."""
        if self.is_alive:
            self.is_sleeping = not self.is_sleeping
            if self.is_sleeping:
                self.energy = min(
                    100.0,  # Max stat is 100
                    self.energy + settings.pet.SLEEP_ENERGY_RECOVERY
                ) 