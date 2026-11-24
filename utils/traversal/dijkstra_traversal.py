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
#external imports
import numpy as np

# PyRat imports
from utils.traversal.traversal import Traversal
from utils.traversal.min_heap import Min_Heap


##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class DijkstraTraversal (Traversal):

    """
    This class implements a Dijkstra traversal algorithm by defining the abstract methods from the parent class.
    We use a FILO hip to indicate the order in which vertices should be explored.
    """

    ##################################################################################
    #                                   CONSTRUCTOR                                  #
    ##################################################################################

    def __init__ ( self,
                   *args:    object,
                   **kwargs: object
                 ) ->        None:

        """
        *(This class inherits from* ``Traversal`` *).*

        It implements a Dijkstra traversal algorithm by defining the abstract methods from the parent class.
        We use a FIFO queue to indicate the order in which vertices should be explored.

        Args:
            args:   Arguments to pass to the parent constructor.
            kwargs: Keyword arguments to pass to the parent constructor.
        """
        
        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # FIFO queue of the elements to visit, as a list, created by initialize_structure
        self.queue = None

    ##################################################################################
    #                                     METHODS                                    #
    ##################################################################################

    def initialize_structure (self) -> None:

        """
        *(This method redefines the method of the parent class with the same name).*

        It initializes the data structure needed for the traversal, and stores it in the ``queue`` attribute.
        Here, we use a list to implement a FIFO queue.
        """

        # We start with an empty list
        self.queue = Min_Heap()
        
    ##################################################################################

    def add_to_structure ( self,
                           element: object
                         ) ->       None:

        """
        *(This method redefines the method of the parent class with the same name).*

        It adds an element to the data structure stored in the ``queue`` attribute.
        Here, we append the element to the end of the list to implement a FIFO queue.

        Args:
            element: The element to add, as a tuple (distance, vertex, parent).
        """

        # We append the element to the end of the list
        self.queue.add_or_replace(element)

    ##################################################################################

    def get_from_structure (self) -> object:

        """
        *(This method redefines the method of the parent class with the same name).*

        It extracts an element from the data structure stored in the ``queue`` attribute.
        Here, we remove and return the first element of the list to implement a FIFO queue.

        Returns:
            The extracted element, as a tuple (distance, vertex, parent).
        """
        return self.queue.remove()



    ##################################################################################

    def is_structure_empty (self) -> bool:

        """
        *(This method redefines the method of the parent class with the same name).*

        It indicates whether the data structure stored in the ``queue`` attribute contains no more elements to extract.
        Here, the FIFO queue is empty when the list has no element.

        Returns:
            True if the data structure is empty, False otherwise.
        """

        # The queue is empty when the list has no element
        return self.queue.get_taille()


##########################################################################################
##########################################################################################