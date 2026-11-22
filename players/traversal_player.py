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

# PyRat imports
from pyrat import Player, Maze, GameState, Action
from utils.traversal.traversal import Traversal
from utils.traversal.bfs_traversal import BFSTraversal

##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class TraversalPlayer (Player):

    """
    *(This class inherits from* ``Player`` *).*

    This player controls a PyRat character that explores the maze using a graph traversal algorithm.
    The traversal algorithm is given at creation, as an object of a subclass of ``Traversal`` (e.g., ``BFSTraversal()``).
    """

    ##################################################################################
    #                                   CONSTRUCTOR                                  #
    ##################################################################################

    def __init__ ( self,
                   traversal_algorithm: Traversal | None = None,
                   *args:               object,
                   **kwargs:            object
                 ) ->                   None:

        """
        Initializes a new instance of the class.
        Here, the constructor is only used to initialize the player.
        It transmits the arguments to the parent constructor, which is responsible for initializing the name and the skin of the player.

        Args:
            traversal_algorithm: The traversal algorithm to use, as an object of a subclass of ``Traversal`` (default is a new ``BFSTraversal``).
                                 Each player needs its own object, as it stores the results of the last traversal.
            args:                Arguments to pass to the parent constructor.
            kwargs:              Keyword arguments to pass to the parent constructor.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # We create an attribute to store the actions to perform
        self.actions = None

        # We store the chosen traversal algorithm, or create the default one
        self.traversal_algorithm = traversal_algorithm if traversal_algorithm is not None else BFSTraversal()

    ##################################################################################
    #                                  PYRAT METHODS                                 #
    ##################################################################################

    def preprocessing ( self,
                        maze:       Maze,
                        game_state: GameState,
                      ) ->          None:
        
        """
        *(This method redefines the method of the parent class with the same name).*

        This method is called once at the beginning of the game.
        Here, we use the traversal algorithm to compute a path that reaches the piece of cheese from the initial position of the player.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.
        """

        # We perform a traversal of the maze graph from the initial position of the player
        my_location = game_state.player_locations[self.get_name()]
        cheese_found = self.traversal_algorithm.traversal(maze, my_location, game_state.cheese)

        # Find the series of locations/actions to go from the player location to the first piece of cheese
        path = self.traversal_algorithm.find_route(cheese_found)
        self.actions = maze.locations_to_actions(path)

    ##################################################################################

    def turn ( self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

        """
        *(This method redefines the method of the parent class with the same name).*

        It is called at each turn of the game.
        It returns an action to perform among the possible actions, defined in the ``Action`` enumeration.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.
        
        Returns:
            One of the possible actions.
        """

        # At each turn, we perform the next action in the list of actions
        return self.actions.pop(0)

##########################################################################################
##########################################################################################