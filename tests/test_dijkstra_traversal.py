##########################################################################################
########################################## INFO ##########################################
##########################################################################################

"""
This program is provided during session 3 of the PyRat project:
https://hub.imt-atlantique.fr/ueinfo-fise1a/s5/project/session3/practical/

We have chosen to organize tests as follows:
- Methods are tested by multiple tests, to have each test focusing on a specific aspect of the method.
- Tests are named test___<tested method>___<test case>___<tested property> (this is a choice, anything named ``test_*`` is fine).
- Random mazes are created once in ``setUpClass(...)``, and shared by all tests, so that each test is as short as possible.

We basically perform two types of tests here:
- On random mazes: To make sure that the methods work as expected in various cases.
                   This allows to test invariants (e.g., the output is of a specific type), but not specific results.
- On manually created mazes: To make sure that the methods work as expected in specific cases.
                             This allows to test specific results (e.g., the output on this particular instance is equal to that specific value).

Also, tests are grouped in three categories:
- Normal use: The method is called as it is meant to be.
- Corner cases: The method is called with valid but unusual inputs (e.g., the smallest possible graph).
- Error cases: The method is called with invalid inputs, and should raise an exception.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import copy
import random
import unittest

# PyRat imports
from pyrat import Graph, RandomMaze, MazeFromDict, PyRatException
from utils.traversal.dijkstra_traversal import DijkstraTraversal


##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class DijkstraTraversal_Tests (unittest.TestCase):

    """
    *(This class inherits from* ``unittest.TestCase`` *).*

    This class tests the methods of the ``DijkstraTraversal`` class.
    For each method, we test it with a few different configurations.
    """

    ##################################################################################
    #                                 INITIALIZATION                                 #
    ##################################################################################

    @classmethod
    def setUpClass (cls) -> None:

        """
        This method is called once, before all test methods.
        Here, we use it to create the mazes, so that they are shared by all tests instead of being created again in each test.
        """

        # A 3x3 maze with no cycle (a tree), with some mud
        # Whatever the algorithm, there is a unique path between any two vertices
        #   [0] --- [1] ~3~ [2]
        #            |
        #   [3] --- [4]     [5]
        #           ~2~     ~5~
        #   [6] --- [7] --- [8]
        cls.tree_maze = MazeFromDict({0: {1: 1},
                                      1: {0: 1, 2: 3, 4: 1},
                                      2: {1: 3},
                                      3: {4: 1},
                                      4: {1: 1, 3: 1, 7: 2},
                                      5: {8: 5},
                                      6: {7: 1},
                                      7: {4: 2, 6: 1, 8: 1},
                                      8: {7: 1, 5: 5}})

        # A 2x2 maze forming a single cycle, with heavy mud on one edge
        # Going directly from 0 to 1 costs 10, while going around (0 -> 2 -> 3 -> 1) costs 3
        #   [0] ~10~ [1]
        #    |        |
        #   [2] ---- [3]
        cls.mud_cycle_maze = MazeFromDict({0: {1: 10, 2: 1},
                                           1: {0: 10, 3: 1},
                                           2: {0: 1, 3: 1},
                                           3: {1: 1, 2: 1}})

        # A maze with two connected components {0, 1} and {2, 3}
        #   [0] --- [1]
        #
        #   [2] --- [3]
        cls.disconnected_maze = MazeFromDict({0: {1: 1},
                                              1: {0: 1},
                                              2: {3: 1},
                                              3: {2: 1}})

        # We use a random number generator (RNG) with a fixed seed, so that tests are reproducible
        rng = random.Random(42)

        # Create 100 random mazes, with no holes
        # We use various sizes and densities, and add some mud so that edges do not all have weight 1
        cls.random_mazes = []
        for _ in range(100):
            cls.random_mazes.append(RandomMaze(width=rng.randint(2, 30),
                                               height=rng.randint(2, 30),
                                               wall_percentage=rng.uniform(20.0, 100.0),
                                               mud_percentage=rng.uniform(0.0, 50.0),
                                               mud_range=(2, 10),
                                               random_seed=rng.randint(0, 2**31 - 1)))

    ##################################################################################

    def setUp (self) -> None:

        """
        This method is called before each test method.
        Here, we use it to instantiate a DijkstraTraversal object.
        """

        # Instantiate a DijkstraTraversal object to test its methods
        self.traversal = DijkstraTraversal()

    ##################################################################################
    #                        TESTS (DijkstraTraversal.traversal)                     #
    ##################################################################################

    def test___dijkstra_traversal___random_mazes___output_types (self) -> None:

        """
        Category: normal use.
        This method tests the ``traversal(...)`` method on random mazes.
        It checks that outputs are of the expected types.
        """

        # Distances should be a dictionary with integer keys and values
        # The routing table should be a dictionary with integer keys and integer or None values
        for maze in self.random_mazes:
            start_vertex = maze.get_vertices()[0]
            self.traversal.traversal(maze, start_vertex)
            distances = self.traversal.get_distances()
            routing_table = self.traversal.get_routing_table()
            self.assertIsInstance(distances, dict, "Distances should be a dictionary")
            self.assertTrue(all(isinstance(k, int) and isinstance(v, int) for k, v in distances.items()), "Distances should have integer keys and values")
            self.assertIsInstance(routing_table, dict, "The routing table should be a dictionary")
            self.assertTrue(all(isinstance(k, int) and isinstance(v, (type(None), int)) for k, v in routing_table.items()), "The routing table should have integer keys, and integer or None values")

    ##################################################################################

    def test___dijkstra_traversal___random_mazes___all_vertices_visited (self) -> None:

        """
        Category: normal use.
        This method tests the ``traversal(...)`` method on random mazes.
        It checks that all vertices are visited, and appear in both outputs.
        This assumes that the maze is connected, which is the case for random mazes generated by PyRat.
        """

        # Both outputs should have the maze vertices as keys
        for maze in self.random_mazes:
            start_vertex = maze.get_vertices()[0]
            self.traversal.traversal(maze, start_vertex)
            distances = self.traversal.get_distances()
            routing_table = self.traversal.get_routing_table()
            self.assertEqual(set(distances.keys()), set(maze.get_vertices()), "Distances should be given for all vertices of the maze, and only for them")
            self.assertEqual(set(routing_table.keys()), set(maze.get_vertices()), "The routing table should contain all vertices of the maze, and only them")

    ##################################################################################

    def test___dijkstra_traversal___random_mazes___routing_table_is_spanning_tree (self) -> None:

        """
        Category: normal use.
        This method tests the ``traversal(...)`` method on random mazes.
        It checks that the routing table is a tree, rooted at the start vertex, that only uses edges of the maze.
        """

        # The start vertex is the root, all other vertices go up to it without cycle, and each parent is a neighbor in the maze
        for maze in self.random_mazes:
            start_vertex = maze.get_vertices()[0]
            self.traversal.traversal(maze, start_vertex)
            routing_table = self.traversal.get_routing_table()
            ancestors = {}
            for vertex in routing_table:
                ancestors[vertex] = set()
                ancestor = routing_table[vertex]
                while ancestor is not None:
                    self.assertNotIn(ancestor, ancestors[vertex], f"The routing table contains a cycle (vertex {ancestor} is met twice when going up from vertex {vertex})")
                    ancestors[vertex].add(ancestor)
                    ancestor = routing_table[ancestor]
            self.assertIsNone(routing_table[start_vertex], "The start vertex should have no parent in the routing table")
            for vertex in routing_table.keys() - {start_vertex}:
                self.assertIn(start_vertex, ancestors[vertex], f"Going up the routing table from vertex {vertex} should lead to the start vertex")
                self.assertIn(routing_table[vertex], maze.get_neighbors(vertex), f"The parent of vertex {vertex} in the routing table should be one of its neighbors in the maze")

    ##################################################################################

    def test___dijkstra_traversal___random_mazes___optimal_distances (self) -> None:

        """
        Category: normal use.
        This method tests the ``traversal(...)`` method on random mazes.
        It checks that computed distances satisfy the shortest path optimality condition (Bellman's inequality):
        for every edge (u, v), distances[v] <= distances[u] + weight(u, v).
        """

        # No edge should allow relaxing an already computed distance
        for maze in self.random_mazes:
            start_vertex = maze.get_vertices()[0]
            self.traversal.traversal(maze, start_vertex)
            distances = self.traversal.get_distances()
            routing_table = self.traversal.get_routing_table()
            self.assertEqual(distances[start_vertex], 0, "The distance to the start vertex should be 0")
            for vertex in routing_table.keys() - {start_vertex}:
                parent = routing_table[vertex]
                self.assertEqual(distances[vertex], distances[parent] + maze.get_weight(parent, vertex), f"The distance to vertex {vertex} should match the path in the routing table")
            for vertex_1, vertex_2 in maze.get_edges():
                weight = maze.get_weight(vertex_1, vertex_2)
                self.assertLessEqual(distances[vertex_2], distances[vertex_1] + weight, f"Edge ({vertex_1}, {vertex_2}) allows a shorter path to {vertex_2}")
                self.assertLessEqual(distances[vertex_1], distances[vertex_2] + weight, f"Edge ({vertex_2}, {vertex_1}) allows a shorter path to {vertex_1}")

    ##################################################################################

    def test___dijkstra_traversal___random_mazes___maze_unchanged (self) -> None:

        """
        Category: normal use.
        This method tests the ``traversal(...)`` method on random mazes.
        It checks that the traversal does not modify the maze.
        """

        # The maze should be the same before and after the traversal
        for maze in self.random_mazes:
            start_vertex = maze.get_vertices()[0]
            maze_before = copy.deepcopy(maze.as_dict())
            self.traversal.traversal(maze, start_vertex)
            self.assertEqual(maze.as_dict(), maze_before, "The traversal should not modify the maze")

    ##################################################################################

    def test___dijkstra_traversal___fixed_mazes___avoids_mud (self) -> None:

        """
        Category: normal use.
        This method tests the ``traversal(...)`` method on manually created mazes with mud.
        Specifically, on ``mud_cycle_maze``, Dijkstra must avoid the direct muddy edge (weight 10)
        and take the longer detour (cost 3).
        """

        # Test on mud_cycle_maze from vertex 0
        self.traversal.traversal(self.mud_cycle_maze, 0)
        self.assertEqual(self.traversal.get_distances(), {0: 0, 2: 1, 3: 2, 1: 3}, "Dijkstra should find the lowest-cost path around the mud")
        self.assertEqual(self.traversal.get_routing_table(), {0: None, 2: 0, 3: 2, 1: 3}, "Routing table should bypass the muddy edge (0, 1)")

        # Test on tree_maze from vertex 4
        self.traversal.traversal(self.tree_maze, 4)
        self.assertEqual(self.traversal.get_distances(), {4: 0, 1: 1, 3: 1, 7: 2, 0: 2, 2: 4, 6: 3, 8: 3, 5: 8})
        self.assertEqual(self.traversal.get_routing_table(), {4: None, 1: 4, 3: 4, 7: 4, 0: 1, 2: 1, 6: 7, 8: 7, 5: 8})

    ##################################################################################

    def test___dijkstra_traversal___single_vertex_graph___only_source_visited (self) -> None:

        """
        Category: corner case.
        This method tests the ``traversal(...)`` method on the smallest possible graph, with a single vertex and no edge.
        """

        # Only the source should be visited
        graph = Graph()
        graph.add_vertex(0)
        self.traversal.traversal(graph, 0)
        self.assertEqual((self.traversal.get_distances(), self.traversal.get_routing_table()), ({0: 0}, {0: None}), "Only the source should be visited in a graph with a single vertex")

    ##################################################################################

    def test___dijkstra_traversal___disconnected_maze___only_component_visited (self) -> None:

        """
        Category: corner case.
        This method tests the ``traversal(...)`` method on a maze that is not connected.
        Only the vertices that can be reached from the source should be visited.
        """

        # Vertices 2 and 3 cannot be reached from 0
        self.traversal.traversal(self.disconnected_maze, 0)
        self.assertEqual((self.traversal.get_distances(), self.traversal.get_routing_table()), ({0: 0, 1: 1}, {0: None, 1: 0}), "Only the vertices reachable from the source should be visited")

    ##################################################################################

    def test___dijkstra_traversal___source_not_in_maze___raises_error (self) -> None:

        """
        Category: error case.
        This method tests the ``traversal(...)`` method when the source is not a vertex of the maze.
        """

        # Cell 9 does not exist in this maze
        with self.assertRaises(PyRatException, msg="A traversal from a vertex that is not in the maze should raise an error"):
            self.traversal.traversal(self.disconnected_maze, 9)

    ##################################################################################

    def test___dijkstra_traversal___graph_not_a_graph___raises_error (self) -> None:

        """
        Category: error case.
        This method tests the ``traversal(...)`` method when the graph is not a PyRat ``Graph``.
        """

        # None and a dictionary do not have a get_neighbors(...) method
        with self.assertRaises(AttributeError, msg="A traversal of None should raise an error"):
            self.traversal.traversal(None, 0)
        with self.assertRaises(AttributeError, msg="A traversal of a dictionary should raise an error"):
            self.traversal.traversal({0: {1: 1}, 1: {0: 1}}, 0)

    ##################################################################################

    def test___dijkstra_traversal___source_wrong_type___raises_error (self) -> None:

        """
        Category: error case.
        This method tests the ``traversal(...)`` method when the source is not an integer.
        """

        # "0" is a string and None is not a vertex
        with self.assertRaises(PyRatException, msg="A traversal from a string should raise an error"):
            self.traversal.traversal(self.disconnected_maze, "0")
        with self.assertRaises(PyRatException, msg="A traversal from None should raise an error"):
            self.traversal.traversal(self.disconnected_maze, None)

    ##################################################################################
    #                       TESTS (DijkstraTraversal.find_route)                     #
    ##################################################################################

    def test___dijkstra_find_route___fixed_mazes___expected_outputs (self) -> None:

        """
        Category: normal use.
        This method tests the ``find_route(...)`` method after a Dijkstra traversal,
        verifying that the reconstructed path avoids heavy mud.
        """

        # Route on mud_cycle_maze from 0 to 1 should go through 2 and 3
        self.traversal.traversal(self.mud_cycle_maze, 0)
        self.assertEqual(self.traversal.find_route(1), [0, 2, 3, 1], "Route from 0 to 1 should avoid the muddy edge")

        # Route on tree_maze from 4 to 5
        self.traversal.traversal(self.tree_maze, 4)
        self.assertEqual(self.traversal.find_route(5), [4, 7, 8, 5], "Wrong route from vertex 4 to vertex 5")

    ##################################################################################

    def test___dijkstra_find_route___source_is_target___single_vertex_route (self) -> None:

        """
        Category: corner case.
        This method tests the ``find_route(...)`` method when the source and the target are the same vertex.
        """

        # Routing table obtained from vertex 4
        self.traversal.traversal(self.tree_maze, 4)
        self.assertEqual(self.traversal.find_route(4), [4], "The route from the root to itself should only contain the root")

    ##################################################################################

    def test___dijkstra_find_route___before_traversal_or_unreachable___raises_error (self) -> None:

        """
        Category: error case.
        This method tests that ``find_route(...)`` raises the expected exceptions when called before
        any traversal or with an unreachable target.
        """

        # Before any traversal
        with self.assertRaises(RuntimeError, msg="Finding a route before any traversal should raise a RuntimeError"):
            self.traversal.find_route(0)

        # Unreachable target in a disconnected maze
        self.traversal.traversal(self.disconnected_maze, 0)
        with self.assertRaises(ValueError, msg="Finding a route to an unreachable vertex should raise a ValueError"):
            self.traversal.find_route(3)


##########################################################################################
######################################### SCRIPT #########################################
##########################################################################################

if __name__ == "__main__":

    # Run all tests
    unittest.main(verbosity=2)

##########################################################################################
##########################################################################################