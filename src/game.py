import tkinter as tk
from tkinter import messagebox
from .tamagotchi import Tamagotchi
import time

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tamagotchi")
        self.root.geometry("400x500")
        
        # Create Tamagotchi instance
        self.pet = Tamagotchi("Tama")
        
        # Create GUI elements
        self.setup_gui()
        
        # Start update loop
        self.update_stats()
    
    def setup_gui(self):
        # Status frame
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=10)
        
        # Name label
        self.name_label = tk.Label(status_frame, text=f"Name: {self.pet.name}", font=("Arial", 14))
        self.name_label.pack()
        
        # Stats labels
        self.hunger_label = tk.Label(status_frame, text="Hunger: 100%")
        self.hunger_label.pack()
        self.happiness_label = tk.Label(status_frame, text="Happiness: 100%")
        self.happiness_label.pack()
        self.energy_label = tk.Label(status_frame, text="Energy: 100%")
        self.energy_label.pack()
        
        # Buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Action buttons
        tk.Button(button_frame, text="Feed", command=self.feed_pet).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Play", command=self.play_with_pet).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Sleep", command=self.toggle_sleep).pack(side=tk.LEFT, padx=5)
        
        # Status message
        self.status_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.status_label.pack(pady=20)
    
    def update_stats(self):
        if not self.pet.is_alive:
            messagebox.showinfo("Game Over", f"{self.pet.name} has passed away...")
            self.root.quit()
            return
        
        self.pet.update()
        
        # Update labels
        self.hunger_label.config(text=f"Hunger: {int(self.pet.hunger)}%")
        self.happiness_label.config(text=f"Happiness: {int(self.pet.happiness)}%")
        self.energy_label.config(text=f"Energy: {int(self.pet.energy)}%")
        
        # Update status message
        status = "Sleeping" if self.pet.is_sleeping else "Awake"
        self.status_label.config(text=f"Status: {status}")
        
        # Schedule next update
        self.root.after(1000, self.update_stats)
    
    def feed_pet(self):
        self.pet.feed()
        messagebox.showinfo("Action", f"Fed {self.pet.name}!")
    
    def play_with_pet(self):
        self.pet.play()
        messagebox.showinfo("Action", f"Played with {self.pet.name}!")
    
    def toggle_sleep(self):
        self.pet.sleep()
        status = "sleeping" if self.pet.is_sleeping else "awake"
        messagebox.showinfo("Action", f"{self.pet.name} is now {status}!")
    
    def run(self):
        self.root.mainloop() 