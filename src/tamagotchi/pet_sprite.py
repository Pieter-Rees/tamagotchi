import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import math

class PetSprite:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.current_frame = 0
        self.animation_frames = []
        self.current_animation = "idle"
        self.animations = {
            "idle": [],
            "happy": [],
            "sleep": [],
            "eat": [],
            "walk": [],
            "play": [],
            "sick": []
        }
        self.sprite_id = None
        self.frame_delay = 150  # milliseconds between frames
        self.load_sprites()
        self.start_animation()

    def create_pixel_art(self, state, frame):
        # Create a larger canvas for more detailed pixel art
        size = (64, 64)
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Base colors for different states
        colors = {
            "idle": "#4CAF50",    # Green
            "happy": "#FFC107",   # Yellow
            "sleep": "#2196F3",   # Blue
            "eat": "#FF5722",     # Orange
            "walk": "#4CAF50",    # Green
            "play": "#FFC107",    # Yellow
            "sick": "#9E9E9E"     # Gray
        }
        
        base_color = colors[state]
        
        # Draw the basic body shape
        body_points = [
            (24, 32),  # Head
            (20, 40),  # Body
            (28, 40),  # Body
            (24, 48),  # Bottom
        ]
        
        # Add animation-specific modifications
        if state == "idle":
            # Gentle breathing animation
            y_offset = math.sin(frame * 0.5) * 2
            body_points = [(x, y + y_offset) for x, y in body_points]
        elif state == "happy":
            # Bouncing animation
            y_offset = math.sin(frame * 0.8) * 3
            body_points = [(x, y + y_offset) for x, y in body_points]
        elif state == "sleep":
            # Sleeping animation with z's
            y_offset = math.sin(frame * 0.3) * 1
            body_points = [(x, y + y_offset) for x, y in body_points]
            # Draw Z's
            if frame % 2 == 0:
                draw.text((32, 20), "z", fill=base_color, font=None)
        elif state == "eat":
            # Eating animation
            y_offset = math.sin(frame * 0.7) * 2
            body_points = [(x, y + y_offset) for x, y in body_points]
        elif state == "walk":
            # Walking animation
            x_offset = math.sin(frame * 0.8) * 3
            body_points = [(x + x_offset, y) for x, y in body_points]
        elif state == "play":
            # Playing animation
            y_offset = math.sin(frame * 0.9) * 4
            x_offset = math.cos(frame * 0.9) * 2
            body_points = [(x + x_offset, y + y_offset) for x, y in body_points]
        elif state == "sick":
            # Sick animation
            y_offset = math.sin(frame * 0.4) * 1
            body_points = [(x, y + y_offset) for x, y in body_points]
        
        # Draw the body
        draw.polygon(body_points, fill=base_color)
        
        # Add eyes
        eye_color = "#FFFFFF"
        if state == "sleep":
            # Closed eyes
            draw.line([(22, 30), (26, 30)], fill=eye_color, width=2)
        else:
            # Open eyes
            draw.ellipse([(22, 28), (24, 30)], fill=eye_color)
            draw.ellipse([(26, 28), (28, 30)], fill=eye_color)
        
        # Add mouth based on state
        if state == "happy":
            # Smile
            draw.arc([(22, 32), (28, 36)], 0, 180, fill="#000000", width=2)
        elif state == "eat":
            # Open mouth
            draw.ellipse([(23, 34), (27, 36)], fill="#000000")
        elif state == "sick":
            # Frown (fixed coordinates to ensure y1 > y0)
            draw.arc([(22, 32), (28, 36)], 180, 360, fill="#000000", width=2)
        else:
            # Neutral mouth
            draw.line([(23, 34), (27, 34)], fill="#000000", width=2)
        
        return ImageTk.PhotoImage(img)

    def load_sprites(self):
        # Create 8 frames for each animation state
        for state in self.animations:
            for frame in range(8):
                photo = self.create_pixel_art(state, frame)
                self.animations[state].append(photo)

    def start_animation(self):
        self.animate()

    def animate(self):
        if self.sprite_id:
            self.canvas.delete(self.sprite_id)
        
        # Get current animation frames
        frames = self.animations[self.current_animation]
        
        # Display current frame
        self.sprite_id = self.canvas.create_image(
            self.x, self.y,
            image=frames[self.current_frame]
        )
        
        # Update frame counter
        self.current_frame = (self.current_frame + 1) % len(frames)
        
        # Schedule next frame
        self.canvas.after(self.frame_delay, self.animate)

    def set_animation(self, animation_name):
        if animation_name in self.animations:
            self.current_animation = animation_name
            self.current_frame = 0 