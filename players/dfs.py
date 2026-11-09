# External imports
import random

# PyRat imports
from pyrat import Player, Maze, GameState, Action

class DFS(Player) : 
    def __init___  ( self,
                   *args:    object,
                   **kwargs: object
                 ) ->        None:
        super().__init__(*args, **kwargs)

        # We create an attribute to keep track of visited cells
        # We will initialize it in the ``preprocessing()`` method to allow the game to be reset
        # Otherwise, the set would keep the cells visited in previous games
        self.visited_cells = None

        # We also create an attribute for the reduced maze
        self.reduced_maze = None
       
    

    def preprocessing ( self,
                        maze:       Maze,
                        game_state: GameState,
                      ) ->          None:
        
        """
        *(This method redefines the method of the parent class with the same name).*

        This method is called once at the beginning of the game.
        Here, we use it to create a reduced maze that contains only the cells that are not dead-ends.
        We define a dead-end as a cell that has only one neighbor and does not contain cheese or the player.
        Note that this is not the best way to define a dead-end, but it is a simple one.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.
        """

        # Initialize visited cells
        self.visited_cells = set()

        # Reduce the maze
        my_location = game_state.player_locations[self.get_name()]
        self.reduced_maze = self.remove_dead_ends(maze, [my_location] + game_state.cheese)

    ##################################################################################

    def turn ( self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

        """
        *(This method redefines the method of the parent class with the same name).*

        It is called at each turn of the game.
        It returns an action to perform among the possible actions, defined in the ``Action`` enumeration.
        We also update the set of visited cells at each turn.
        Now, we work with the reduced maze to find the next action.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.
        
        Returns:
            One of the possible actions.
        """

        # Mark current cell as visited
        my_location = game_state.player_locations[self.get_name()]
        if my_location not in self.visited_cells:
            self.visited_cells.add(my_location)

        # Return an action
        action = self.find_next_action(self.reduced_maze, game_state)
        return action


    def traversal ( self,
                graph:  Graph,
                source: int
              ) ->      tuple[dict[int, int], dict[int, int | None]]:

        """
        This method performs a DFS traversal of a graph.
        It returns the explored vertices with associated distances.
        The distance to a vertex is the sum of the weights of the edges along the path found (given by ``graph.get_weight(...)``).
        It also returns the routing table, that is, the parent of each vertex in the traversal.

        Args:
            graph:  The graph to traverse.
            source: The source vertex of the traversal (we type it as int here because we will only manipulate mazes, but Graph uses Hashable as a more generic type).

        Returns:
            A tuple containing:
            - The distances from the source to each explored vertex.
            - The routing table, that is, the parent of each vertex in the traversal (None for the source).
        """

        # Your code here
    
   
