import tkinter as tk
from tkinter import messagebox, filedialog
import os
from src.tamagotchi.core.pet import Tamagotchi
from src.tamagotchi.pet_sprite import PetSprite
from src.tamagotchi.config.settings import settings

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(settings.game.TITLE)
        self.root.geometry(f"{settings.game.WINDOW_WIDTH}x{settings.game.WINDOW_HEIGHT}")
        self.root.configure(bg=settings.game.BLACK)
        
        # Create menu bar
        self.create_menu()
        
        # Create main frame with rounded corners
        self.main_frame = tk.Frame(
            self.root,
            bg=settings.game.BLACK,
            highlightthickness=2,
            highlightbackground=settings.game.GRAY
        )
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create canvas for pet
        self.canvas = tk.Canvas(
            self.main_frame,
            width=settings.game.WINDOW_WIDTH - 40,
            height=300,
            bg=settings.game.BLACK,
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        
        # Create status frame
        self.status_frame = tk.Frame(
            self.main_frame,
            bg=settings.game.BLACK,
            highlightthickness=1,
            highlightbackground=settings.game.GRAY
        )
        self.status_frame.pack(fill='x', padx=20, pady=10)
        
        # Create status bars
        self.create_status_bar("Hunger", 0, settings.game.RED)
        self.create_status_bar("Happiness", 1, settings.game.YELLOW)
        self.create_status_bar("Energy", 2, settings.game.GREEN)
        
        # Create buttons frame
        self.buttons_frame = tk.Frame(
            self.main_frame,
            bg=settings.game.BLACK,
            highlightthickness=1,
            highlightbackground=settings.game.GRAY
        )
        self.buttons_frame.pack(fill='x', padx=20, pady=10)
        
        # Configure grid layout for buttons
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)
        self.buttons_frame.grid_columnconfigure(2, weight=1)
        
        # Create buttons with Tamagotchi-like style
        feed_button = self.create_button("Feed", self.feed_pet, 0)
        play_button = self.create_button("Play", self.play_with_pet, 1)
        sleep_button = self.create_button("Sleep", self.sleep_pet, 2)
        
        # Store button references
        self.feed_button = feed_button
        self.play_button = play_button
        self.sleep_button = sleep_button
        
        # Load or create pet
        self.pet = self.load_or_create_pet()
        
        # Create pet sprite
        self.pet_sprite = PetSprite(
            self.canvas,
            settings.game.WINDOW_WIDTH // 2,
            150
        )
        
        # Start game loop
        self.update()
        
    def create_menu(self):
        """Create the menu bar with game options."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Pet", command=self.new_pet)
        file_menu.add_command(label="Load Pet", command=self.load_pet)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_game)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def new_pet(self):
        """Start a new pet."""
        if messagebox.askyesno("New Pet", "Are you sure you want to start a new pet? Your current pet will be saved."):
            self.save_pet()  # Save current pet before creating new one
            self.pet = Tamagotchi("Tama")
            self.save_pet()
            messagebox.showinfo("New Pet", "A new pet has been created!")
            
    def load_pet(self):
        """Load a pet from a save file."""
        save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saves")
        if not os.path.exists(save_dir):
            messagebox.showwarning("Load Pet", "No save directory found!")
            return
            
        # Get list of save files
        save_files = [f for f in os.listdir(save_dir) if f.endswith('.json')]
        if not save_files:
            messagebox.showwarning("Load Pet", "No save files found!")
            return
            
        # Create a dialog to select a save file
        dialog = tk.Toplevel(self.root)
        dialog.title("Load Pet")
        dialog.geometry("300x200")
        dialog.configure(bg=settings.game.BLACK)
        
        # Create a listbox with save files
        listbox = tk.Listbox(
            dialog,
            bg=settings.game.DARK_GRAY,
            fg=settings.game.WHITE,
            selectbackground=settings.game.GRAY,
            selectforeground=settings.game.BLACK
        )
        listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        for save_file in save_files:
            listbox.insert(tk.END, save_file.replace('.json', ''))
            
        def load_selected():
            selection = listbox.curselection()
            if selection:
                pet_name = listbox.get(selection[0])
                self.save_pet()  # Save current pet
                self.pet = Tamagotchi.load(pet_name, save_dir)
                if self.pet:
                    messagebox.showinfo("Load Pet", f"Loaded {pet_name}!")
                    dialog.destroy()
                else:
                    messagebox.showerror("Load Pet", "Failed to load pet!")
                    
        # Add load button
        load_button = tk.Button(
            dialog,
            text="Load",
            command=load_selected,
            bg=settings.game.GRAY,
            fg=settings.game.BLACK,
            activebackground=settings.game.DARK_GRAY,
            activeforeground=settings.game.WHITE
        )
        load_button.pack(pady=10)
        
    def exit_game(self):
        """Exit the game with confirmation."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit? Your pet will be saved."):
            self.save_pet()
            self.root.quit()
            
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About Tamagotchi",
            "Tamagotchi Game\n\n"
            "A virtual pet game where you can feed, play with, and take care of your pet.\n\n"
            "Created with Python and Tkinter"
        )
        
    def create_status_bar(self, label, row, color):
        frame = tk.Frame(self.status_frame, bg=settings.game.BLACK)
        frame.grid(row=row, column=0, sticky='ew', padx=5, pady=5)
        
        label = tk.Label(
            frame,
            text=label,
            font=('Arial', settings.ui.FONT_SIZE_SMALL),
            bg=settings.game.BLACK,
            fg=settings.game.WHITE,
            width=10
        )
        label.pack(side='left')
        
        bar = tk.Canvas(
            frame,
            width=settings.ui.BAR_WIDTH,
            height=settings.ui.BAR_HEIGHT,
            bg=settings.game.DARK_GRAY,
            highlightthickness=0
        )
        bar.pack(side='left', padx=5)
        
        setattr(self, f"{label.cget('text').lower()}_bar", bar)
        
    def create_button(self, text, command, column):
        """Create a button with the given text, command, and column position."""
        print(f"Creating button: {text} at column {column}")  # Debug print
        
        button = tk.Button(
            self.buttons_frame,
            text=text,
            command=command,
            font=('Arial', settings.ui.FONT_SIZE_SMALL),
            width=10,
            bg=settings.game.GRAY,
            fg=settings.game.BLACK,
            activebackground=settings.game.DARK_GRAY,
            activeforeground=settings.game.WHITE,
            relief=tk.RAISED,
            borderwidth=2
        )
        
        # Place button in grid with padding
        button.grid(row=0, column=column, padx=10, pady=10, sticky='ew')
        
        print(f"Button {text} created and placed at column {column}")  # Debug print
        return button
        
    def update_status_bars(self):
        # Update hunger bar
        self.hunger_bar.delete("all")
        self.hunger_bar.create_rectangle(
            0, 0,
            settings.ui.BAR_WIDTH * (self.pet.hunger / 100),
            settings.ui.BAR_HEIGHT,
            fill=settings.game.RED
        )
        
        # Update happiness bar
        self.happiness_bar.delete("all")
        self.happiness_bar.create_rectangle(
            0, 0,
            settings.ui.BAR_WIDTH * (self.pet.happiness / 100),
            settings.ui.BAR_HEIGHT,
            fill=settings.game.YELLOW
        )
        
        # Update energy bar
        self.energy_bar.delete("all")
        self.energy_bar.create_rectangle(
            0, 0,
            settings.ui.BAR_WIDTH * (self.pet.energy / 100),
            settings.ui.BAR_HEIGHT,
            fill=settings.game.GREEN
        )
        
    def update(self):
        self.pet.update()
        self.update_status_bars()
        self.save_pet()
        
        # Update pet sprite based on state
        if self.pet.is_sleeping:
            self.pet_sprite.set_animation("sleep")
        elif self.pet.happiness > 80:
            self.pet_sprite.set_animation("happy")
        elif self.pet.hunger < 20:
            self.pet_sprite.set_animation("sick")
        else:
            self.pet_sprite.set_animation("idle")
        
        self.root.after(1000, self.update)
        
    def feed_pet(self):
        if not self.pet.is_sleeping:
            self.pet.feed()
            self.pet_sprite.set_animation("eat")
            self.root.after(1000, lambda: self.pet_sprite.set_animation("idle"))
        else:
            messagebox.showwarning("Warning", "Cannot feed while sleeping!")
        
    def play_with_pet(self):
        if self.pet.is_sleeping:
            messagebox.showwarning("Warning", "Cannot play while sleeping!")
            return
            
        if self.pet.energy >= settings.pet.PLAY_ENERGY_COST:
            self.pet.play()
            self.pet_sprite.set_animation("play")
            self.root.after(1000, lambda: self.pet_sprite.set_animation("idle"))
        else:
            messagebox.showwarning("Warning", "Not enough energy to play!")
            
    def sleep_pet(self):
        """Toggle sleep mode for the pet."""
        self.pet.sleep()
        if self.pet.is_sleeping:
            self.pet_sprite.set_animation("sleep")
            messagebox.showinfo("Sleep", f"{self.pet.name} is now sleeping.")
        else:
            self.pet_sprite.set_animation("idle")
            messagebox.showinfo("Sleep", f"{self.pet.name} has woken up.")
        
    def load_or_create_pet(self):
        save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saves")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, "tama.json")
        
        print(f"Load directory: {save_dir}")
        print(f"Attempting to load from: {save_path}")
        
        # Try to load existing pet
        pet = Tamagotchi.load("tama", save_dir)
        if pet is not None:
            return pet
            
        print(f"No save file found at: {save_path}")
        # Create new pet if none exists
        pet = Tamagotchi("Tama")
        pet.save(save_dir)
        return pet
            
    def save_pet(self):
        try:
            save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saves")
            self.pet.save(save_dir)
        except Exception as e:
            print(f"Error saving pet: {e}")
            messagebox.showerror("Error", "Failed to save pet state!")
            
    def run(self):
        self.root.mainloop() 