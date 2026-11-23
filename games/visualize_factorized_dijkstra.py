##########################################################################################
########################################## INFO ##########################################
##########################################################################################

"""
This program is provided during session 2 of the PyRat project:
https://hub.imt-atlantique.fr/ueinfo-fise1a/s5/project/session2/practical/
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import pprint

# PyRat imports
from pyrat import Game
from players.traversal_player import TraversalPlayer
from utils.traversal.dijkstra_traversal import DijkstraTraversal

##########################################################################################
######################################### SCRIPT #########################################
##########################################################################################

if __name__ == "__main__":

    # Instantiate a game with a few arguments
    game_config = {"mud_percentage": 30.0,
                   "maze_width": 13,
                   "maze_height": 10,
                   "nb_cheese": 1,
                   "random_seed": 2,
                   "trace_length": 1000}

    # Instantiate a game with specified arguments
    game = Game(**game_config)

    # Instantiate the player
    player = TraversalPlayer(DijkstraTraversal(), name="Factorized Dijkstra")
    game.add_player(player)

    # Start the game
    stats = game.start()
    pprint.pprint(stats)

##########################################################################################
##########################################################################################