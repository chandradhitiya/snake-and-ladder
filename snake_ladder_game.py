#!/usr/bin/env python3
# Snake and Ladder Game
# Author: Chandradhitiya
# License: MIT

import random
import time
import os
import sys

class SnakeAndLadderGame:
    def __init__(self):
        # Game board size
        self.board_size = 100
        
        # Define snakes (head -> tail)
        self.snakes = {
            16: 6,
            47: 26,
            49: 11,
            56: 53,
            62: 19,
            64: 60,
            87: 24,
            93: 73,
            95: 75,
            98: 78
        }
        
        # Define ladders (bottom -> top)
        self.ladders = {
            1: 38,
            4: 14,
            9: 31,
            21: 42,
            28: 84,
            36: 44,
            51: 67,
            71: 91,
            80: 100
        }
        
        # Player positions
        self.players = {}
        self.player_names = []

    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_board(self):
        """Display the game board with current player positions."""
        self.clear_screen()
        print("\n🎮 SNAKE 🐍 AND LADDER 🪜 GAME 🎮\n")
        
        # Create a visual representation of the board
        board = []
        # Initialize with empty spaces
        for i in range(10):
            row = ["     " for _ in range(10)]
            board.append(row)
        
        # Fill in the numbers
        for i in range(100):
            row = 9 - (i // 10)
            col = i % 10 if (i // 10) % 2 == 0 else 9 - (i % 10)
            cell_num = i + 1
            cell_str = f"{cell_num:3d}  "
            board[row][col] = cell_str
        
        # Mark snakes and ladders
        for head, tail in self.snakes.items():
            row = 9 - ((head-1) // 10)
            col = (head-1) % 10 if ((head-1) // 10) % 2 == 0 else 9 - ((head-1) % 10)
            board[row][col] = f"{head:3d}🐍 "
            
        for bottom, top in self.ladders.items():
            row = 9 - ((bottom-1) // 10)
            col = (bottom-1) % 10 if ((bottom-1) // 10) % 2 == 0 else 9 - ((bottom-1) % 10)
            board[row][col] = f"{bottom:3d}🪜 "
        
        # Add player positions
        for player, position in self.players.items():
            if position == 0:  # Not on board yet
                continue
                
            row = 9 - ((position-1) // 10)
            col = (position-1) % 10 if ((position-1) // 10) % 2 == 0 else 9 - ((position-1) % 10)
            
            # Update the cell to show player
            current_cell = board[row][col]
            player_symbol = player[0].upper()
            
            if "🐍" in current_cell or "🪜" in current_cell:
                # Keep the snake or ladder symbol
                board[row][col] = f"{position:3d}{current_cell[3]}{player_symbol}"
            else:
                board[row][col] = f"{position:3d} {player_symbol}"
        
        # Print the board
        print("+" + "----------+" * 10)
        for row in board:
            print("|" + "|".join(row) + "|")
            print("+" + "----------+" * 10)
            
        # Print player positions
        print("\nPlayer Positions:")
        for player, position in self.players.items():
            position_str = position if position > 0 else "Not started"
            print(f"  {player}: {position_str}")
        print()

    def roll_dice(self):
        """Roll a dice and return the value."""
        return random.randint(1, 6)

    def move_player(self, player, steps):
        """Move a player by the given number of steps."""
        current_position = self.players[player]
        new_position = current_position + steps
        
        # Check if player can move (must be exactly 100 to win)
        if new_position > 100:
            print(f"{player} rolled too high. Staying at position {current_position}.")
            return current_position
            
        # Update position
        self.players[player] = new_position
        
        # Check if landed on a snake
        if new_position in self.snakes:
            print(f"Oh no! {player} got bitten by a snake at {new_position}! 🐍")
            time.sleep(1)
            self.players[player] = self.snakes[new_position]
            print(f"Moving down to {self.players[player]}.")
            
        # Check if landed on a ladder
        elif new_position in self.ladders:
            print(f"Great! {player} found a ladder at {new_position}! 🪜")
            time.sleep(1)
            self.players[player] = self.ladders[new_position]
            print(f"Climbing up to {self.players[player]}.")
            
        return self.players[player]

    def setup_players(self):
        """Set up players for the game."""
        while True:
            try:
                num_players = int(input("Enter number of players (2-4): "))
                if 2 <= num_players <= 4:
                    break
                else:
                    print("Please enter a number between 2 and 4.")
            except ValueError:
                print("Please enter a valid number.")
        
        for i in range(num_players):
            name = input(f"Enter name for Player {i+1}: ")
            self.player_names.append(name)
            self.players[name] = 0

    def play(self):
        """Start and play the game."""
        # Setup
        self.setup_players()
        current_player_idx = 0
        winner = None
        
        # Game loop
        while winner is None:
            self.display_board()
            
            current_player = self.player_names[current_player_idx]
            input(f"{current_player}'s turn. Press Enter to roll the dice...")
            
            dice_roll = self.roll_dice()
            print(f"{current_player} rolled a {dice_roll}.")
            time.sleep(1)
            
            # First roll must be 6 to start
            if self.players[current_player] == 0 and dice_roll != 6:
                print(f"{current_player} needs to roll a 6 to start. Try again next turn!")
            else:
                # If this is the first valid roll, set position to 1 (start)
                if self.players[current_player] == 0:
                    print(f"{current_player} rolled a 6 and enters the game!")
                    self.players[current_player] = 1
                    # Move only the remaining 5 steps (1 was used to enter)
                    new_position = self.move_player(current_player, dice_roll - 1)
                else:
                    new_position = self.move_player(current_player, dice_roll)
                
                print(f"{current_player} moved to position {new_position}.")
                
                # Check for winner
                if new_position == 100:
                    winner = current_player
            
            # Next player's turn
            time.sleep(1)
            current_player_idx = (current_player_idx + 1) % len(self.player_names)
        
        # Game finished
        self.display_board()
        print(f"🎉 Congratulations! {winner} won the game! 🎉")

if __name__ == "__main__":
    game = SnakeAndLadderGame()
    game.play()