#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
This file contains the implementation of the Dijkstra traversal algorithm using an unsorted list as its priority queue structure.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# PyRat imports
from utils.traversal.traversal import Traversal

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class ListDijkstraTraversal (Traversal):

    """
    A class implementing the Dijkstra traversal algorithm using an unsorted Python list instead of a binary min-heap.
    Insertion appends or updates elements in O(V) time, while extraction scans the full list to retrieve the minimum distance element in O(V) time.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self,
                   *args:    object,
                   **kwargs: object
                 ) ->        None:

        """
        Initializes a new instance of the class.

        Args:
            args:   Arguments to pass to the parent constructor.
            kwargs: Keyword arguments to pass to the parent constructor.
        """

        # Call the parent constructor
        super().__init__(*args, **kwargs)

        # Initialize the structure attribute
        self.structure = None

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def initialize_structure (self) -> None:

        """
        Initializes the routing table structure as an empty list.
        """

        self.structure = []

    #############################################################################################################################################

    def add_to_structure ( self,
                           element: tuple[int, int]
                         ) ->       None:

        """
        Adds a vertex and its associated distance to the unsorted list, or updates its distance if a shorter path is found.

        Args:
            element: Tuple of the form (vertex, distance) to insert or update in the structure.
        """

        # Unpack vertex and distance
        vertex, distance = element

        # Update the distance if the vertex is already present in the list
        for i in range(len(self.structure)):
            if self.structure[i][0] == vertex:
                if distance < self.structure[i][1]:
                    self.structure[i] = (vertex, distance)
                return

        # Otherwise append the new element at the end of the list
        self.structure.append((vertex, distance))

    #############################################################################################################################################

    def get_from_structure (self) -> tuple[int, int]:

        """
        Finds, removes, and returns the element with the smallest distance by scanning the entire unsorted list.

        Returns:
            Tuple of the form (vertex, distance) corresponding to the minimum distance element.

        Raises:
            IndexError: If the structure is empty when attempting to extract an element.
        """

        # Raise an explicit error if the structure is empty
        if self.is_structure_empty():
            raise IndexError("Cannot pop from an empty list structure.")

        # Scan the list to find the index of the minimum distance element
        min_index = 0
        for i in range(1, len(self.structure)):
            if self.structure[i][1] < self.structure[min_index][1]:
                min_index = i

        # Remove and return the minimum element
        return self.structure.pop(min_index)

    #############################################################################################################################################

    def is_structure_empty (self) -> bool:

        """
        Checks whether the unsorted list structure contains any remaining elements.

        Returns:
            True if the list is empty, False otherwise.
        """

        return len(self.structure) == 0

#####################################################################################################################################################
#####################################################################################################################################################