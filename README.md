# Tamagotchi Game

A simple Tamagotchi virtual pet game implemented in Python using Tkinter.

## Features

- Virtual pet with hunger, happiness, and energy stats
- Interactive GUI with buttons for feeding, playing, and sleeping
- Real-time stat updates
- Game over conditions when pet's needs aren't met

## Requirements

- Python 3.x
- Tkinter (included in standard Python installation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tamagotchi.git
cd tamagotchi
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Running the Game

To start the game, simply run:
```bash
python main.py
```

## Game Controls

- **Feed**: Increases hunger and slightly increases happiness
- **Play**: Significantly increases happiness but decreases energy and hunger
- **Sleep**: Toggles sleep mode and restores energy

## Game Rules

- Your pet's stats (hunger, happiness, energy) decrease over time
- If hunger or happiness reaches 0, your pet will die
- Sleeping restores energy but prevents other actions
- Keep your pet alive by managing its needs!

## Running Tests

To run the test suite:
```bash
python -m unittest tests/test_tamagotchi.py
```

## Contributing

Feel free to submit issues and enhancement requests! 