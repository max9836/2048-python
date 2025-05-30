# 2048 game: a simple puzzle game
# Copyright (C) 2025  Max9836 GITHUB

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Reference list:
#
# [Colour Reference] https://github.com/yangshun/2048-python -> in constants.py 
# [Reference] https://codewithcurious.com/projects/2048-game-using-python/ 
# **AI was partly used while developing this program**

import os
import customtkinter as ctk
import random
from tkinter import messagebox

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.root.geometry("900x950")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.grid = [[0 for _ in range(4)] for _ in range(4)] # [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.score = 0
        self.file = file()
        self.high_score = self.file.load_high_score()
        self.game_over = False
        self.create_widgets()
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid()
        self.root.bind("<Key>", self.key_pressed)
        
    def create_widgets(self):
        self.header_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.header_frame.pack(pady=15, padx=25, fill="x")
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="2048", 
            font=("Helvetica", 36, "bold")
        )
        self.title_label.pack(side="left", padx=15, pady=10)
        
        # Score frame
        self.score_frame = ctk.CTkFrame(self.header_frame, corner_radius=5)
        self.score_frame.pack(side="right", padx=15, pady=10)
        
        self.score_label = ctk.CTkLabel(
            self.score_frame, 
            text=f"Score: {self.score}", 
            font=("Helvetica", 16)
        )
        self.score_label.pack(padx=15, pady=8)
        
        # High score frame
        self.high_score_frame = ctk.CTkFrame(self.header_frame, corner_radius=5)
        self.high_score_frame.pack(side="right", padx=15, pady=10)
        
        self.high_score_label = ctk.CTkLabel(
            self.high_score_frame, 
            text=f"High Score: {self.high_score}", 
            font=("Helvetica", 16)
        )
        self.high_score_label.pack(padx=15, pady=8)
        
        # Game grid frame
        self.grid_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.grid_frame.pack(pady=15, padx=25)
        
        # Create grid buttons (larger tiles)
        self.tiles = []
        for i in range(4):
            row = []
            for j in range(4):
                tile = ctk.CTkButton(
                    self.grid_frame, 
                    text="", 
                    width=120,
                    height=120,
                    corner_radius=8,
                    font=("Helvetica", 28, "bold"),
                    fg_color="#cdc1b4",
                    hover=False
                )
                tile.grid(row=i, column=j, padx=8, pady=8)
                row.append(tile)
            self.tiles.append(row)
        
        self.restart_button = ctk.CTkButton(
            self.root, 
            text="New Game", 
            command=self.restart_game,
            font=("Ariel", 16, "bold"),
            width=190,
            height=60,
            corner_radius=25
        )

        self.how_to_play_button = ctk.CTkButton(
            self.root, 
            text="How to Play", 
            command=lambda: messagebox.showinfo("How to Play", "Use arrow keys or WASD to move tiles. Combine tiles with the same number to create a larger tile. Reach 2048 to win!"),
            font=("Ariel", 16, "bold"),
            width=190,
            height=60,
            corner_radius=25
        )

        # Credits, DO NOT CHANGE
        self.credits = ctk.CTkLabel(
            self.root, 
            text="Made by Max9836@GITHUB\nLICENSED UNDER GPLv3",
            text_color="gray", 
            font=("Ariel", 12)
        )

        self.restart_button.pack(pady=10)
        self.how_to_play_button.pack(pady=10)
        self.credits.pack(pady=10)
    
    def get_tile_color(self, value):
        colors = {
            0: "#cdc1b4",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
            4096: "#3c3a32",
            8192: "#2a2924",
            16384: "#1e1d19",
            32768: "#141310",
            65536: "#0a0908"
        }
        # For values beyond our defined colors, use the darkest one
        return colors.get(value, "#000000")
    
    def get_text_color(self, value):
        return "#776e65" if value < 8 else "#f9f6f2"
    
    def update_grid(self):
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                tile = self.tiles[i][j]
                
                # Adjust font size for very large numbers
                font_size = 28
                if value >= 10000:
                    font_size = 20
                elif value >= 1000:
                    font_size = 24
                
                tile.configure(
                    text=str(value) if value != 0 else "",
                    fg_color=self.get_tile_color(value),
                    text_color=self.get_text_color(value),
                    font=("Helvetica", font_size, "bold")
                )
        
        # Update score labels
        self.score_label.configure(text=f"Score: {self.score}")
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.configure(text=f"High Score: {self.high_score}")
            self.file.save_high_score(self.high_score)
    
    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
    
    def move_left(self):
        moved = False
        for i in range(4):
            row = [num for num in self.grid[i] if num != 0]
            new_row = []
            j = 0
            while j < len(row):
                if j + 1 < len(row) and row[j] == row[j + 1]:
                    new_row.append(row[j] * 2)
                    self.score += row[j] * 2
                    j += 2
                    moved = True
                else:
                    new_row.append(row[j])
                    j += 1
            
            new_row += [0] * (4 - len(new_row))
            
            if self.grid[i] != new_row:
                moved = True
            
            self.grid[i] = new_row
        
        return moved
    
    def move_right(self):
        moved = False
        for i in range(4):
            row = [num for num in self.grid[i] if num != 0]
            new_row = []
            
            j = len(row) - 1
            while j >= 0:
                if j - 1 >= 0 and row[j] == row[j - 1]:
                    new_row.insert(0, row[j] * 2)
                    self.score += row[j] * 2
                    j -= 2
                    moved = True
                else:
                    new_row.insert(0, row[j])
                    j -= 1
            
            new_row = [0] * (4 - len(new_row)) + new_row
            
            if self.grid[i] != new_row:
                moved = True
            
            self.grid[i] = new_row
        
        return moved
    
    def move_up(self):
        moved = False
        for j in range(4):
            column = [self.grid[i][j] for i in range(4) if self.grid[i][j] != 0]
            new_column = []
            
            i = 0
            while i < len(column):
                if i + 1 < len(column) and column[i] == column[i + 1]:
                    new_column.append(column[i] * 2)
                    self.score += column[i] * 2
                    i += 2
                    moved = True
                else:
                    new_column.append(column[i])
                    i += 1
            
            new_column += [0] * (4 - len(new_column))
            
            for i in range(4):
                if self.grid[i][j] != new_column[i]:
                    moved = True
                self.grid[i][j] = new_column[i]
        
        return moved
    
    def move_down(self):
        moved = False
        for j in range(4):
            column = [self.grid[i][j] for i in range(4) if self.grid[i][j] != 0]
            new_column = []
            
            i = len(column) - 1
            while i >= 0:
                if i - 1 >= 0 and column[i] == column[i - 1]:
                    new_column.insert(0, column[i] * 2)
                    self.score += column[i] * 2
                    i -= 2
                    moved = True
                else:
                    new_column.insert(0, column[i])
                    i -= 1
            
            new_column = [0] * (4 - len(new_column)) + new_column
            
            for i in range(4):
                if self.grid[i][j] != new_column[i]:
                    moved = True
                self.grid[i][j] = new_column[i]
        
        return moved
    
    def is_game_over(self):
        # Check if there are empty cells
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return False
        
        # Check for possible merges
        for i in range(4):
            for j in range(3):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return False
        
        for j in range(4):
            for i in range(3):
                if self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        
        return True
    
    def key_pressed(self, event):
        if self.game_over:
            return
        
        moved = False
        if event.keysym in ('Left', 'a', 'A'):
            moved = self.move_left()
        elif event.keysym in ('Right', 'd', 'D'):
            moved = self.move_right()
        elif event.keysym in ('Up', 'w', 'W'):
            moved = self.move_up()
        elif event.keysym in ('Down', 's', 'S'):
            moved = self.move_down()
        
        # Check valid move
        if moved:
            self.add_new_tile()
            self.update_grid()

            for i in range(4):
                for j in range(4):
                    if self.grid[i][j] == 2048:
                        answer = messagebox.askyesno("You won!", "Congratulations! You reached 2048!\nDo you want to continue playing?")
                        if not answer:
                            self.file.save_high_score(self.score)
                            self.game_over = True
                        return
            
            if self.is_game_over():
                self.game_over = True
                answer = messagebox.askyesno("Game Over", f"Game Over! Your score: {self.score}\nDo you want to restart the game?")
                if answer:
                    self.restart_game()
                return
    
    def restart_game(self):
        # Reset the game state
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid()

#   file class to handle high score
class file:
    def __init__(self):
        self.highscore_file = "highscore.dat"

    def save_high_score(self, score):
        """Save high score as plain text."""
        with open(self.highscore_file, "w") as f:
            f.write(str(score))

    def load_high_score(self):
        """Load high score as plain text."""
        if not os.path.exists(self.highscore_file):
            return 0
        with open(self.highscore_file, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                messagebox.showerror("Error", "Invalid high score file. Resetting to 0.")
                return 0
            
if __name__ == "__main__":
    root = ctk.CTk()
    game = Game(root)
    root.mainloop()
