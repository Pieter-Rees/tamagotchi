from typing import Dict, Optional
import tkinter as tk
from tkinter import ttk
import time
from ..core.pet import Tamagotchi
from ..config.settings import settings

class Game:
    """Main game class handling the tkinter interface and game loop."""
    
    def __init__(self) -> None:
        """Initialize the game window and UI elements."""
        self.root = tk.Tk()
        self.root.title(settings.game.TITLE)
        self.root.geometry(f"{settings.game.WINDOW_WIDTH}x{settings.game.WINDOW_HEIGHT}")
        
        # Game state
        self.pet: Optional[Tamagotchi] = None
        self.input_active = False
        self.input_text = ""
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create UI elements
        self._create_widgets()
        
        # Start with new pet
        self.create_new_pet()
        
        # Start update loop
        self._update()

    def _create_widgets(self) -> None:
        """Create all UI widgets."""
        # Pet name label
        self.name_label = ttk.Label(
            self.main_frame,
            text="",
            font=("", settings.ui.FONT_SIZE_LARGE)
        )
        self.name_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Status label
        self.status_label = ttk.Label(
            self.main_frame,
            text="",
            font=("", settings.ui.FONT_SIZE_LARGE)
        )
        self.status_label.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Status bars
        self.hunger_bar = ttk.Progressbar(
            self.main_frame,
            length=settings.ui.BAR_WIDTH,
            mode='determinate'
        )
        self.hunger_bar.grid(row=2, column=0, columnspan=3, pady=5)
        self.hunger_label = ttk.Label(self.main_frame, text="Hunger: 100")
        self.hunger_label.grid(row=2, column=0, columnspan=3, sticky=tk.W)
        
        self.happiness_bar = ttk.Progressbar(
            self.main_frame,
            length=settings.ui.BAR_WIDTH,
            mode='determinate'
        )
        self.happiness_bar.grid(row=3, column=0, columnspan=3, pady=5)
        self.happiness_label = ttk.Label(self.main_frame, text="Happiness: 100")
        self.happiness_label.grid(row=3, column=0, columnspan=3, sticky=tk.W)
        
        self.energy_bar = ttk.Progressbar(
            self.main_frame,
            length=settings.ui.BAR_WIDTH,
            mode='determinate'
        )
        self.energy_bar.grid(row=4, column=0, columnspan=3, pady=5)
        self.energy_label = ttk.Label(self.main_frame, text="Energy: 100")
        self.energy_label.grid(row=4, column=0, columnspan=3, sticky=tk.W)
        
        # Buttons
        self.feed_button = ttk.Button(
            self.main_frame,
            text="Feed",
            command=self._on_feed
        )
        self.feed_button.grid(row=5, column=0, padx=5, pady=20)
        
        self.play_button = ttk.Button(
            self.main_frame,
            text="Play",
            command=self._on_play
        )
        self.play_button.grid(row=5, column=1, padx=5, pady=20)
        
        self.sleep_button = ttk.Button(
            self.main_frame,
            text="Sleep",
            command=self._on_sleep
        )
        self.sleep_button.grid(row=5, column=2, padx=5, pady=20)
        
        self.new_pet_button = ttk.Button(
            self.main_frame,
            text="New Pet",
            command=self.create_new_pet
        )
        self.new_pet_button.grid(row=6, column=0, columnspan=3, pady=10)
        
        # Input frame
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.grid(row=7, column=0, columnspan=3, pady=20)
        
        self.input_label = ttk.Label(
            self.input_frame,
            text="Enter pet name:",
            font=("", settings.ui.FONT_SIZE_SMALL)
        )
        self.input_label.grid(row=0, column=0, pady=5)
        
        self.input_entry = ttk.Entry(
            self.input_frame,
            width=20,
            font=("", settings.ui.FONT_SIZE_SMALL)
        )
        self.input_entry.grid(row=1, column=0, pady=5)
        self.input_entry.bind('<Return>', self._on_name_enter)
        
        # Initially hide input frame
        self.input_frame.grid_remove()

    def create_new_pet(self) -> None:
        """Reset the game state for a new pet."""
        self.input_active = True
        self.input_text = ""
        self.pet = None
        
        # Show input frame and hide other elements
        self.input_frame.grid()
        self.name_label.grid_remove()
        self.status_label.grid_remove()
        self.hunger_bar.grid_remove()
        self.hunger_label.grid_remove()
        self.happiness_bar.grid_remove()
        self.happiness_label.grid_remove()
        self.energy_bar.grid_remove()
        self.energy_label.grid_remove()
        self.feed_button.grid_remove()
        self.play_button.grid_remove()
        self.sleep_button.grid_remove()
        self.new_pet_button.grid_remove()
        
        # Clear and focus input
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus()

    def _on_name_enter(self, event: Optional[tk.Event] = None) -> None:
        """Handle pet name entry."""
        name = self.input_entry.get().strip()
        if name:
            self.pet = Tamagotchi(name)
            self.input_active = False
            
            # Hide input frame and show other elements
            self.input_frame.grid_remove()
            self.name_label.grid()
            self.status_label.grid()
            self.hunger_bar.grid()
            self.hunger_label.grid()
            self.happiness_bar.grid()
            self.happiness_label.grid()
            self.energy_bar.grid()
            self.energy_label.grid()
            self.feed_button.grid()
            self.play_button.grid()
            self.sleep_button.grid()
            self.new_pet_button.grid()

    def _on_feed(self) -> None:
        """Handle feed button click."""
        if self.pet and self.pet.is_alive and not self.pet.is_sleeping:
            self.pet.feed()

    def _on_play(self) -> None:
        """Handle play button click."""
        if self.pet and self.pet.is_alive and not self.pet.is_sleeping:
            self.pet.play()

    def _on_sleep(self) -> None:
        """Handle sleep button click."""
        if self.pet and self.pet.is_alive:
            self.pet.sleep()

    def _update(self) -> None:
        """Update game state and UI."""
        if self.pet:
            self.pet.update()
            
            # Update UI
            self.name_label.config(text=self.pet.name)
            self.status_label.config(
                text="Sleeping..." if self.pet.is_sleeping else "Awake"
            )
            
            # Update status bars
            self.hunger_bar['value'] = self.pet.hunger
            self.hunger_label.config(text=f"Hunger: {int(self.pet.hunger)}")
            
            self.happiness_bar['value'] = self.pet.happiness
            self.happiness_label.config(text=f"Happiness: {int(self.pet.happiness)}")
            
            self.energy_bar['value'] = self.pet.energy
            self.energy_label.config(text=f"Energy: {int(self.pet.energy)}")
            
            # Update button states
            state = 'normal' if self.pet.is_alive and not self.pet.is_sleeping else 'disabled'
            self.feed_button['state'] = state
            self.play_button['state'] = state
            
            # Show death message if pet died
            if not self.pet.is_alive:
                self.status_label.config(
                    text="Your pet has passed away...",
                    foreground='red'
                )
                self.feed_button.grid_remove()
                self.play_button.grid_remove()
                self.sleep_button.grid_remove()
                self.new_pet_button.grid()
        
        # Schedule next update
        self.root.after(1000 // settings.game.FPS, self._update)

    def run(self) -> None:
        """Start the game."""
        self.root.mainloop()

def run_game() -> None:
    """Run the game."""
    game = Game()
    game.run() 