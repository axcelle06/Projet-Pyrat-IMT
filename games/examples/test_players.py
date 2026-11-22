# PyRat imports
from pyrat import Game
from players.randoms.random1 import Random1 
from players.randoms.random2 import Random2
from players.randoms.random3 import Random3

if __name__=='__main__':
    """
    # Instantiate a game with a few arguments
    game = Game(maze_width=2, maze_height=2, nb_cheese=1)

    # Instantiate the player
    # If we do not specify a name, the player will be named "Random1"
    player = Random1()
    game.add_player(player)

    # Start the game
    stats = game.start()
    """



    """
    # Instantiate a game with a few arguments
    game = Game(maze_width=15, maze_height=13, nb_cheese=1)

    # Instantiate the player
    # If we do not specify a name, the player will be named "Random2"
    player = Random2()
    game.add_player(player)

    # Start the game
    stats = game.start()

    """



    game = Game(maze_width=15, maze_height=13, nb_cheese=1)

    # Instantiate the player
    # If we do not specify a name, the player will be named "Random3"
    player = Random3()
    game.add_player(player)

    # Start the game
    stats = game.start()
