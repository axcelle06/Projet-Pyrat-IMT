# PyRat imports
from pyrat import Game
from players.random4 import Random4
if __name__ == "__main__":  
# Instantiate a game with a few arguments
    game = Game(maze_width=8, maze_height=8, nb_cheese=1, cell_percentage=70.0)

# Instantiate the player
# If we do not specify a name, the player will be named "Random4"
    player = Random4()
    game.add_player(player)

# Start the game
    stats = game.start()