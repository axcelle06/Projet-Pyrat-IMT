# PyRat imports
from pyrat import Game
from players.randoms.random3 import Random3
if __name__ == "__main__":
# Instantiate a game with a few arguments
    game = Game(maze_width=8, maze_height=8, nb_cheese=1)

# Instantiate the player
# If we do not specify a name, the player will be named "Random3"
    player = Random3()
    game.add_player(player)

# Start the game
    stats = game.start()