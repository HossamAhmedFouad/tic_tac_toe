"""
Author:Hossam Ahmed Fouad
Version: 1.0
Date: 3-2-2022
"""

# importing Game class from game python file
from game import Game

# creating tic tac toe as a Game Object
tic_tac_toe = Game()

# Main Loop That Keeps The Game Running
while tic_tac_toe.running:
    # Displaying Menus and launching game loop
    tic_tac_toe.curr_menu.display_menu()
    tic_tac_toe.game_loop()

