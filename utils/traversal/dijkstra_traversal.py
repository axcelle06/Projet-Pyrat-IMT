# PyRat imports
from utils.traversal.min_heap import Min_Heap
from utils.traversal.traversal import Traversal


##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class DijkstraTraversal (Traversal):

    """
    This class implements a Dijkstra traversal algorithm by defining the abstract methods from the parent class.
    We use a MIN-heap to indicate the order in which vertices should be explored.
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
        We use a MIN-heap to indicate the order in which vertices should be explored.

        Args:
            args:   Arguments to pass to the parent constructor.
            kwargs: Keyword arguments to pass to the parent constructor.
        """
        
        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # MIN-heap of the elements to visit, as a Min_Heap object, created by initialize_structure
        self.structure = None

    ##################################################################################
    #                                     METHODS                                    #
    ##################################################################################

    def initialize_structure (self) -> None:

        """
        *(This method redefines the method of the parent class with the same name).*

        It initializes the data structure needed for the traversal, and stores it in the ``structure`` attribute.
        Here, we use a list to implement a MIN-heap.
        """

        # We start with an empty list
        self.structure = Min_Heap()

    ##################################################################################

    def add_to_structure ( self,
                            element: tuple[int, int]
                         ) ->       None:

        """
        *(This method redefines the method of the parent class with the same name).*

        It adds an element to the data structure stored in the ``structure`` attribute.
        Here, we insert the element into the MIN-heap.

        Args:
            element: The element to add, as a tuple (key, value).
        """

        # We insert the element into the MIN-heap
        self.structure.add_or_replace(element)

    ##################################################################################

    def get_from_structure (self) -> object:

        """
        *(This method redefines the method of the parent class with the same name).*

        It extracts an element from the data structure stored in the ``structure`` attribute.
        Here, we remove and return the element with the smallest key from the MIN-heap.

        Returns:
            The extracted element, as a tuple (key, value).
        """

        # We remove and return the element with the smallest value from the MIN-heap
        return self.structure.remove()
    ##################################################################################

    def is_structure_empty (self) -> bool:

        """
        *(This method redefines the method of the parent class with the same name).*

        It indicates whether the data structure stored in the ``structure`` attribute contains no more elements to extract.
        Here, the min-heap is empty when the list has no element.

        Returns:
            True if the data structure is empty, False otherwise.
        """

        # The structure is empty when the min-heap has no element
        return self.structure.get_taille() == 0


##########################################################################################
##########################################################################################