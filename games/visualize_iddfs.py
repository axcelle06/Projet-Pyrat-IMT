# External imports
import pprint

# PyRat imports
from pyrat import Game, StartingLocation
from players.iddfs import IDDFS


##########################################################################################
######################################### SCRIPT #########################################
##########################################################################################

if __name__ == "__main__":
    game_config = {"mud_percentage": 0.0,
                   "maze_width": 13,
                   "maze_height": 10,
                   "nb_cheese": 5,
                   "trace_length": 1000}

    # Instantiate a game with specified arguments
    game = Game(**game_config)
    
    player = IDDFS()
    game.add_player(player, location=StartingLocation.BOTTOM_LEFT)


    stats = game.start()
    print(f"Statistics for {player.get_name()}:")
    pprint.pprint(stats)

    # Reset the game for the next player
    # Argument same=True means that the game will keep the same maze and cheese distribution
    game.reset(keep_players=False, same=True)

##########################################################################################
##########################################################################################
