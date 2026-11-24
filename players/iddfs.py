# External imports
import random
import numpy as np

# PyRat imports
from pyrat import Player, Maze, GameState, Action, Graph

class IDDFS(Player) : 

    # TODO : -étudier le comportement du dfs sur plusieurs labyrinthes (notamment voir ce qu'il se passe pour plusieurs froamges ?)
    #        -mettre la méthode remove dead_ends sur le dfs pour optimiser le preprocessing


    def __init___  ( self, *args:    object,  **kwargs: object ) ->        None:
        super().__init__(*args, **kwargs)
        self.visited_cells = None #setup dans préprocessing
        self.reduced_maze = None #labyrinthe optimisé sans les dead ends
        self.actions = None #liste d'action (enum north south east west)
    

    def preprocessing ( self, maze: Maze, game_state: GameState) -> None:
        
        """
        Reduce le labyrinthe pour enlever les dead ends
        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.
        """

        # Initialize visited cells
        self.visited_cells = set()
        self.actions = []
        remaining_cheese = set(game_state.cheese)
        my_location = game_state.player_locations[self.get_name()]

        while len(remaining_cheese)>0:
            _, routing_table, cheese = self.traversal(maze,my_location, remaining_cheese )
            chemin_fromage = self.find_route(routing_table, my_location, cheese)
            self.actions += [maze.locations_to_action(chemin_fromage[i],chemin_fromage[i+1]) for i in range(len(chemin_fromage)-1)]
            my_location = cheese
            remaining_cheese.remove(cheese)


        # Reduce the maze
        #self.reduced_maze = self.remove_dead_ends(maze, [my_location] + game_state.cheese)
        #On considère ici qu'on prend les fromages dans l'ordre où ils sont dans game_state, à opti plus tard ?


        

    ##################################################################################
     
    def turn ( self, maze: Maze, game_state: GameState) -> Action:
        """
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
        action = self.actions[0]
        self.actions = self.actions[1:]
        return action


    def traversal ( self, graph:  Graph, source: int, objectifs = None ) -> tuple[dict[int, int], dict[int, int | None], int]:
        # https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search
        #note : j'ai mis table de routage= {} et ça buggait parce que l'argument restait en mémoire donc à l'appel d'une autre fonction ça utilisait les valeurs de l'argument de l'appel précédent !! ducoup bien mettre None
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
        def DLS(node,depth):
                    if depth == 0:
                        if node in objectifs:
                            return (node, True)
                        else:
                            return (None, True) #not found but may have children
                    else: #on considere depth>0 en entrée
                        any_remaining = False
                        for voisin in graph.get_neighbors(node):
                            if voisin not in sommets_visites:
        
                                rooting_table[voisin] = node
                                sommets_visites[voisin] = graph.get_weight(voisin,node) + sommets_visites[node]
                                
                                found, remaining = DLS(voisin, depth-1)
                                if found is not None:
                                    return (found, True)
                                if remaining:
                                    any_remaining = True
                        return (None, any_remaining)
                    
        depth = 0
        remaining = True
        while remaining:
            sommets_visites = {source : 0}
            rooting_table = {source : None}
            found, remaining = DLS(source, depth)
            
            if found is not None:
                return sommets_visites, rooting_table, found

            depth+=1
        return sommets_visites, rooting_table, None
        
        
    
        

    def find_route ( self, routing_table: dict[int, int | None], source: int, target:int) -> list[int]:
        #pas d'ia utilisée
        """
        This method finds the route from a source vertex to a target vertex using a routing table.

        Args:
            routing_table: The routing table, that is, the parent of each vertex in the traversal (None for the source) ({sommet : parent}).
            source:        The source vertex.
            target:        The target vertex.

        Returns:
            The route from the source to the target as a list of vertices.
        """
        if not isinstance(routing_table,dict):
            raise TypeError("La table de routage doit etre de type dict[int, int|None]")
        
        if target not in routing_table:
            raise KeyError("La source ou la target n'est pas dans le graphe")
        
        if target==source:
            return [source]
        
        parent = routing_table[target]
        if parent is None:
            raise KeyError("Aucun chemin entre la source et la target")
        return self.find_route(routing_table, source, parent)+[target]




    