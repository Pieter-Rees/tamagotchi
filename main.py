import os
import sys

print("=== Starting Tamagotchi Game ===")
print(f"Current working directory: {os.getcwd()}")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

from src.game import Game

if __name__ == "__main__":
    print("Creating game instance...")
    game = Game()
    print("Starting game...")
    game.run() 