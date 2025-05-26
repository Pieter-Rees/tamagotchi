from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
import time
import json
import os
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

    def save(self, save_dir: str = "saves") -> None:
        """Save the pet's state to a file."""
        try:
            # Get absolute path to save directory
            save_dir = os.path.abspath(save_dir)
            print(f"Save directory: {save_dir}")
            
            # Ensure save directory exists
            if not os.path.exists(save_dir):
                print(f"Creating save directory: {save_dir}")
                os.makedirs(save_dir, exist_ok=True)
            
            # Convert pet data to dictionary
            pet_data = asdict(self)
            
            # Save to file
            save_path = os.path.join(save_dir, f"{self.name.lower()}.json")
            print(f"Saving to: {save_path}")
            
            # Ensure we have write permissions
            if os.path.exists(save_path) and not os.access(save_path, os.W_OK):
                print(f"Warning: No write permission for {save_path}")
                return
            
            # Write the save file
            with open(save_path, 'w') as f:
                json.dump(pet_data, f)
            print(f"Successfully saved pet to: {save_path}")
            
            # Verify the file was created
            if os.path.exists(save_path):
                print(f"Verified save file exists at: {save_path}")
            else:
                print(f"Warning: Save file was not created at: {save_path}")
            
        except Exception as e:
            print(f"Error saving pet: {str(e)}")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Save directory: {save_dir}")
            print(f"Save path: {save_path if 'save_path' in locals() else 'Not created'}")
            raise  # Re-raise the exception to be handled by the caller

    @classmethod
    def load(cls, name: str, save_dir: str = "saves") -> Optional['Tamagotchi']:
        """Load a pet's state from a file."""
        try:
            # Get absolute path to save directory
            save_dir = os.path.abspath(save_dir)
            print(f"Load directory: {save_dir}")
            
            save_path = os.path.join(save_dir, f"{name.lower()}.json")
            print(f"Attempting to load from: {save_path}")
            
            if not os.path.exists(save_path):
                print(f"No save file found at: {save_path}")
                return None
            
            # Check read permissions
            if not os.access(save_path, os.R_OK):
                print(f"Warning: No read permission for {save_path}")
                return None
                
            with open(save_path, 'r') as f:
                pet_data = json.load(f)
            
            print(f"Successfully loaded pet from: {save_path}")
            return cls(**pet_data)
            
        except Exception as e:
            print(f"Error loading pet: {str(e)}")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Save directory: {save_dir}")
            print(f"Save path: {save_path if 'save_path' in locals() else 'Not created'}")
            return None

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