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
import abc

# PyRat imports
from pyrat import Graph

##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class Traversal (abc.ABC):

    """
    This is an abstract class that defines the interface for graph traversal algorithms.
    It is meant to be inherited by specific traversal algorithm implementations, such as breadth-first search (BFS) or depth-first search (DFS).
    
    Each subclass chooses the data structure that stores the vertices to visit, and keeps it as it wishes.
    The traversal only manipulates it through four abstract methods that must be implemented in the subclasses:
        * ``initialize_structure``: Initializes the data structure needed for the traversal.
        * ``add_to_structure``: Adds an element to the data structure.
        * ``get_from_structure``: Extracts an element from the data structure.
        * ``is_structure_empty``: Indicates whether the data structure is empty.
    The choice of data structure (e.g., queue, stack) will determine the behavior of the traversal algorithm.
    """

    ##################################################################################
    #                                   CONSTRUCTOR                                  #
    ##################################################################################

    def __init__ ( self,
                   *args:    object,
                   **kwargs: object
                 ) ->        None:

        """
        *(This class is abstract and meant to be subclassed, not instantiated directly).*

        Initializes a new instance of the class.

        Args:
            args:   Arguments to pass to the parent constructor.
            kwargs: Keyword arguments to pass to the parent constructor.
        """
        
        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # Calling traversal will set these attributes
        self.routing_table = None
        self.distances = None

    ##################################################################################
    #                                     METHODS                                    #
    ##################################################################################

    def get_distances (self) -> dict[int, int]:

        """
        This method returns the distances computed by the last traversal.

        Returns:
            The distance from the source to each vertex explored, as a dictionary.
        """

        # Return the distances found
        return self.distances

    ##################################################################################

    def get_routing_table (self) -> dict[int, int | None]:

        """
        This method returns the routing table computed by the last traversal.

        Returns:
            The parent of each vertex explored, as a dictionary (None for the source).
        """

        # Return the routing table found
        return self.routing_table

    ##################################################################################

    def traversal ( self, graph:  Graph, source: int, liste_sommets = None) ->      None:

        """
        This method performs a traversal of the given graph from the given source vertex.
        It computes the distances from the source to all other vertices, as well as a routing table that can be used to reconstruct paths.
        The distance to a vertex is the sum of the weights of the edges along the path found (given by ``graph.get_weight(...)``).
        The results are stored in the ``distances`` and ``routing_table`` attributes.
        
        Args:
            graph:  The graph to traverse.
            source: The source vertex of the traversal (we type it as int here because we will only manipulate mazes, but Graph uses Hashable as a more generic type).
        """

        # Initialization
        self.initialize_structure()
        self.distances = {source : 0}
        self.routing_table = {source : None}
        # If the source is in the list of vertices to explore, we return it immediately
        if liste_sommets is not None and source in liste_sommets:
                return source
        # We add the source to the data structure with a distance of 0
        self.add_to_structure((source,0))

        while not self.is_structure_empty():
            parent, dist_parent = self.get_from_structure()
            # If the parent is in the list of vertices to explore, we return it immediately
            if liste_sommets is not None and parent in liste_sommets:
                return parent
            for voisin in graph.get_neighbors(parent):
                new_distance = graph.get_weight(parent,voisin) + dist_parent
                if voisin not in self.distances or new_distance < self.distances[voisin]:
                        self.distances[voisin] = new_distance
                        self.routing_table[voisin] = parent
                        self.add_to_structure((voisin, new_distance))


        return None
    ##################################################################################

    def find_route ( self, target: int ) -> list[int]:

        """
        This method finds the route from the source vertex to a target vertex using a routing table.

        Args:
            target: The target vertex.

        Returns:
            The route from the source to the target as a list of vertices.

        Raises:
            RuntimeError: If no traversal has been performed yet.
            ValueError: If the target was not reached by the last traversal (e.g., it is in another component of the graph).
        """

        # A route can only be found from the results of a traversal
        if self.routing_table is None:
            raise RuntimeError(f"Cannot find a route to {target!r}: no traversal has been performed yet")

        # The target must have been reached by the traversal
        if target not in self.routing_table:
            raise ValueError(f"Cannot find a route to {target!r}: it was not reached by the last traversal")

        parent = self.routing_table[target]
        if parent is None:
            return [target]
        return self.find_route(parent)+[target]
        

    ##################################################################################

    @abc.abstractmethod
    def initialize_structure (self) -> None:

        """
        *(This method is abstract and must be implemented in the subclasses).*

        It initializes the data structure needed for the traversal.

        Raises:
            NotImplementedError: If called through ``super()``, as a subclass that does not redefine this method cannot be instantiated.
        """

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError(f"{type(self).__name__} must redefine method 'initialize_structure' of Traversal")

    ##################################################################################

    @abc.abstractmethod
    def add_to_structure ( self,
                           element: object
                         ) ->       None:

        """
        *(This method is abstract and must be implemented in the subclasses).*

        It adds an element to the data structure.

        Args:
            element: The element to add, as a tuple (distance, vertex, parent).

        Raises:
            NotImplementedError: If called through ``super()``, as a subclass that does not redefine this method cannot be instantiated.
        """

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError(f"{type(self).__name__} must redefine method 'add_to_structure' of Traversal")

    ##################################################################################

    @abc.abstractmethod
    def get_from_structure (self) -> object:

        """
        *(This method is abstract and must be implemented in the subclasses).*

        It extracts an element from the data structure.

        Returns:
            The extracted element, as a tuple (distance, vertex, parent).

        Raises:
            NotImplementedError: If called through ``super()``, as a subclass that does not redefine this method cannot be instantiated.
        """

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError(f"{type(self).__name__} must redefine method 'get_from_structure' of Traversal")

    ##################################################################################

    @abc.abstractmethod
    def is_structure_empty (self) -> bool:

        """
        *(This method is abstract and must be implemented in the subclasses).*

        It indicates whether the data structure contains no more elements to extract.

        Returns:
            True if the data structure is empty, False otherwise.

        Raises:
            NotImplementedError: If called through ``super()``, as a subclass that does not redefine this method cannot be instantiated.
        """

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError(f"{type(self).__name__} must redefine method 'is_structure_empty' of Traversal")

##########################################################################################
##########################################################################################