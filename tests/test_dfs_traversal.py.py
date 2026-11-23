# External imports
import copy
import random
import unittest

# PyRat imports
from pyrat import Graph, RandomMaze, MazeFromDict, PyRatException
from utils.traversal.dfs_traversal import DFSTraversal



##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class DFSTraversal_Tests (unittest.TestCase):

    """
    *(This class inherits from* ``unittest.TestCase`` *).*

    This class tests the methods of the DFS class.
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
        # Whatever the order of exploration, there is a unique routing table for a given start
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

        # A 2x2 maze forming a single cycle, with no mud
        # A DFS has to go around the cycle, in one direction or the other
        #   [0] --- [1]
        #    |       |
        #   [2] --- [3]
        cls.cycle_maze = MazeFromDict({0: {1: 1, 2: 1},
                                       1: {0: 1, 3: 1},
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
        Here, we use it to instantiate a DFS player.
        """

        # Instantiate a DFS player to test its methods
        self.traversal = DFSTraversal()

    ##################################################################################
    #                              TESTS (dfs.traversal)                             #
    ##################################################################################

    def test___dfs_traversal___random_mazes___output_types (self) -> None:

        """
        Category: normal use.
        This method tests the ``traversal(...)`` method on random mazes.
        It checks that outputs are of the expected types.
        """

        # Distances should be a dictionary with integer keys and values
        # The routing table should be a dictionary with integer keys and integer or None values
        for maze in self.random_mazes:
            start_vertex = maze.get_vertices()[0]
            distances, routing_table = self.player.traversal(maze, start_vertex)
            self.assertIsInstance(distances, dict, "Distances should be a dictionary")
            self.assertTrue(all(isinstance(k, int) and isinstance(v, int) for k, v in distances.items()), "Distances should have integer keys and values")
            self.assertIsInstance(routing_table, dict, "The routing table should be a dictionary")
            self.assertTrue(all(isinstance(k, int) and isinstance(v, (type(None), int)) for k, v in routing_table.items()), "The routing table should have integer keys, and integer or None values")

    ##################################################################################

    def test___dfs_traversal___random_mazes___all_vertices_visited (self) -> None:

        """
        Category: normal use.
        This method tests the ``traversal(...)`` method on random mazes.
        It checks that all vertices are visited, and appear in both outputs.
        This assumes that the maze is connected, which is the case for random mazes generated by PyRat.
        """

        # Both outputs should have the maze vertices as keys
        for maze in self.random_mazes:
            start_vertex = maze.get_vertices()[0]
            distances, routing_table = self.player.traversal(maze, start_vertex)
            self.assertEqual(set(distances.keys()), set(maze.get_vertices()), "Distances should be given for all vertices of the maze, and only for them")
            self.assertEqual(set(routing_table.keys()), set(maze.get_vertices()), "The routing table should contain all vertices of the maze, and only them")

    ##################################################################################

    def test___dfs_traversal___random_mazes___routing_table_is_spanning_tree (self) -> None:

        """
        Category: normal use.
        This method tests the ``traversal(...)`` method on random mazes.
        It checks that the routing table is a tree, rooted at the start vertex, that only uses edges of the maze.
        """

        # The start vertex is the root, all other vertices go up to it without cycle, and each parent is a neighbor in the maze
        # To check this, we go up from each vertex to the root, to find all its ancestors in the tree
        for maze in self.random_mazes:
            start_vertex = maze.get_vertices()[0]
            _, routing_table = self.player.traversal(maze, start_vertex)
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

    def test___dfs_traversal___random_mazes___distances_match_routing_table (self) -> None:

        """
        Category: normal use.
        This method tests the ``traversal(...)`` method on random mazes.
        It checks that distances are 0 for the start vertex, and strictly positive for all other vertices.
        It also checks that they are increasing along the routing table, and more precisely that the distance to each vertex is the distance to its parent plus the weight of the edge between them.
        Since mazes contain mud, this also checks that edge weights are taken into account.
        """

        # The start vertex is at distance 0, and the distance increases by the weight of each edge in the routing table
        for maze in self.random_mazes:
            start_vertex = maze.get_vertices()[0]
            distances, routing_table = self.player.traversal(maze, start_vertex)
            self.assertEqual(distances[start_vertex], 0, "The distance to the start vertex should be 0")
            for vertex in routing_table.keys() - {start_vertex}:
                parent = routing_table[vertex]
                self.assertGreater(distances[vertex], 0, f"The distance to vertex {vertex} should be strictly positive")
                self.assertGreater(distances[vertex], distances[parent], f"The distance to vertex {vertex} should be greater than the distance to its parent {parent}")
                self.assertEqual(distances[vertex], distances[parent] + maze.get_weight(parent, vertex), f"The distance to vertex {vertex} should be the distance to its parent {parent} plus the weight of the edge between them")

    ##################################################################################

    def test___dfs_traversal___random_mazes___is_depth_first (self) -> None:

        """
        Category: normal use.
        This method tests the ``traversal(...)`` method on random mazes.
        It checks that the routing table is indeed a depth-first search tree, and not just any tree.
        Previous tests would also pass with a BFS, for instance.

        In an undirected graph, a DFS tree has the following property: every edge of the graph connects a vertex to one of its ancestors in the tree.
        Indeed, when the DFS explores a vertex, it does not leave it before all its neighbors have been visited.
        A BFS does not have this property, since it can create edges between vertices of different branches.
        """

        # Each edge of the maze should connect a vertex to one of its ancestors
        # To check this, we go up from each vertex to the root, to find all its ancestors in the tree
        for maze in self.random_mazes:
            start_vertex = maze.get_vertices()[0]
            _, routing_table = self.player.traversal(maze, start_vertex)
            ancestors = {}
            for vertex in routing_table:
                ancestors[vertex] = set()
                ancestor = routing_table[vertex]
                while ancestor is not None:
                    self.assertNotIn(ancestor, ancestors[vertex], f"The routing table contains a cycle (vertex {ancestor} is met twice when going up from vertex {vertex})")
                    ancestors[vertex].add(ancestor)
                    ancestor = routing_table[ancestor]
            for vertex_1, vertex_2 in maze.get_edges():
                self.assertTrue(vertex_1 in ancestors[vertex_2] or vertex_2 in ancestors[vertex_1], f"Edge ({vertex_1}, {vertex_2}) connects two different branches of the routing table, which cannot happen in a DFS")

    ##################################################################################

    def test___dfs_traversal___random_mazes___maze_unchanged (self) -> None:

        """
        Category: normal use.
        This method tests the ``traversal(...)`` method on random mazes.
        It checks that the traversal does not modify the maze.
        """

        # The maze should be the same before and after the traversal
        for maze in self.random_mazes:
            start_vertex = maze.get_vertices()[0]
            maze_before = copy.deepcopy(maze.as_dict())
            self.player.traversal(maze, start_vertex)
            self.assertEqual(maze.as_dict(), maze_before, "The traversal should not modify the maze")

    ##################################################################################

    def test___dfs_traversal___fixed_mazes___expected_outputs (self) -> None:

        """
        Category: normal use.
        This method tests the ``traversal(...)`` method on some manually created mazes.
        In general, a DFS has multiple valid outputs, depending on the order in which neighbors are explored.
        Here, we choose mazes for which we can list all valid outputs (see the ``setUpClass(...)`` method).
        """

        # Test cases, with all valid outputs (distances, routing table) for each of them
        TESTS = [{"maze": self.tree_maze,
                  "start": 4,
                  "outputs": [({4: 0, 1: 1, 3: 1, 7: 2, 0: 2, 2: 4, 6: 3, 8: 3, 5: 8},
                               {4: None, 1: 4, 3: 4, 7: 4, 0: 1, 2: 1, 6: 7, 8: 7, 5: 8})]},
                 {"maze": self.tree_maze,
                  "start": 0,
                  "outputs": [({0: 0, 1: 1, 2: 4, 4: 2, 3: 3, 7: 4, 6: 5, 8: 5, 5: 10},
                               {0: None, 1: 0, 2: 1, 4: 1, 3: 4, 7: 4, 6: 7, 8: 7, 5: 8})]},
                 {"maze": self.cycle_maze,
                  "start": 0,
                  "outputs": [({0: 0, 1: 1, 3: 2, 2: 3}, {0: None, 1: 0, 3: 1, 2: 3}),
                              ({0: 0, 2: 1, 3: 2, 1: 3}, {0: None, 2: 0, 3: 2, 1: 3})]}]

        # Outputs should match one of the expected ones
        for test in TESTS:
            outputs = self.player.traversal(test["maze"], test["start"])
            self.assertIn(outputs, test["outputs"], f"Unexpected outputs for a traversal from vertex {test['start']}")

    ##################################################################################

    def test___dfs_traversal___single_vertex_graph___only_source_visited (self) -> None:

        """
        Category: corner case.
        This method tests the ``traversal(...)`` method on the smallest possible graph, with a single vertex and no edge.
        PyRat mazes need at least two cells, so we use a graph here.
        """

        # Only the source should be visited
        graph = Graph()
        graph.add_vertex(0)
        self.assertEqual(self.player.traversal(graph, 0), ({0: 0}, {0: None}), "Only the source should be visited in a graph with a single vertex")

    ##################################################################################

    def test___dfs_traversal___disconnected_maze___only_component_visited (self) -> None:

        """
        Category: corner case.
        This method tests the ``traversal(...)`` method on a maze that is not connected.
        Only the vertices that can be reached from the source should be visited.
        """

        # Vertices 2 and 3 cannot be reached from 0
        self.assertEqual(self.player.traversal(self.disconnected_maze, 0), ({0: 0, 1: 1}, {0: None, 1: 0}), "Only the vertices reachable from the source should be visited")

    ##################################################################################

    def test___dfs_traversal___source_not_in_maze___raises_error (self) -> None:

        """
        Category: error case.
        This method tests the ``traversal(...)`` method when the source is not a vertex of the maze.
        PyRat raises a ``PyRatException`` when asking for the neighbors of a vertex that does not exist.
        """

        # Cell 9 does not exist in this maze
        with self.assertRaises(PyRatException, msg="A traversal from a vertex that is not in the maze should raise an error"):
            self.player.traversal(self.disconnected_maze, 9)

    ##################################################################################

    def test___dfs_traversal___graph_not_a_graph___raises_error (self) -> None:

        """
        Category: error case.
        This method tests the ``traversal(...)`` method when the graph is not a PyRat ``Graph`` (unexpected argument).
        The error is raised by Python when trying to call ``get_neighbors(...)`` on an object that does not have this method.
        """

        # None and a dictionary do not have a get_neighbors(...) method
        with self.assertRaises(AttributeError, msg="A traversal of None should raise an error"):
            self.player.traversal(None, 0)
        with self.assertRaises(AttributeError, msg="A traversal of a dictionary should raise an error, even if it describes a graph"):
            self.player.traversal({0: {1: 1}, 1: {0: 1}}, 0)

    ##################################################################################

    def test___dfs_traversal___source_wrong_type___raises_error (self) -> None:

        """
        Category: error case.
        This method tests the ``traversal(...)`` method when the source is not an integer (unexpected argument).
        Such a source cannot be a vertex of the maze, so PyRat raises a ``PyRatException``, as when the source does not exist.
        """

        # "0" is a string, not the integer 0
        with self.assertRaises(PyRatException, msg="A traversal from a string should raise an error"):
            self.player.traversal(self.disconnected_maze, "0")
        with self.assertRaises(PyRatException, msg="A traversal from None should raise an error"):
            self.player.traversal(self.disconnected_maze, None)

    ##################################################################################
    #                             TESTS (dfs.find_route)                             #
    ##################################################################################

    def test___dfs_find_route___random_mazes___output_types (self) -> None:

        """
        Category: normal use.
        This method tests the ``find_route(...)`` method on random mazes.
        It checks that the output is a list of integers.
        """

        # The route should be a list of integers
        for maze in self.random_mazes:
            start_vertex, target_vertex = maze.get_vertices()[0], maze.get_vertices()[-1]
            _, routing_table = self.player.traversal(maze, start_vertex)
            route = self.player.find_route(routing_table, start_vertex, target_vertex)
            self.assertIsInstance(route, list, "The route should be a list")
            self.assertTrue(all(isinstance(v, int) for v in route), "The route should only contain integers")

    ##################################################################################

    def test___dfs_find_route___random_mazes___follows_routing_table (self) -> None:

        """
        Category: normal use.
        This method tests the ``find_route(...)`` method on random mazes.
        It checks that the route goes from the start to the target, following the routing table.
        Since the routing table is a tree of the maze (tested above), the route is then a path in the maze with no repeated vertex.
        """

        # The route starts at the start, ends at the target, and each vertex is the parent of the next one
        for maze in self.random_mazes:
            start_vertex, target_vertex = maze.get_vertices()[0], maze.get_vertices()[-1]
            _, routing_table = self.player.traversal(maze, start_vertex)
            route = self.player.find_route(routing_table, start_vertex, target_vertex)
            self.assertEqual(route[0], start_vertex, "The route should start at the start vertex")
            self.assertEqual(route[-1], target_vertex, "The route should end at the target vertex")
            self.assertTrue(all(routing_table[route[j + 1]] == route[j] for j in range(len(route) - 1)), "Each vertex of the route should be the parent of the next one in the routing table")

    ##################################################################################

    def test___dfs_find_route___random_mazes___routing_table_unchanged (self) -> None:

        """
        Category: normal use.
        This method tests the ``find_route(...)`` method on random mazes.
        It checks that finding a route does not modify the routing table.
        This is important, since the same routing table may be used to find routes to multiple targets.
        """

        # The routing table should be the same before and after finding the route
        for maze in self.random_mazes:
            start_vertex, target_vertex = maze.get_vertices()[0], maze.get_vertices()[-1]
            _, routing_table = self.player.traversal(maze, start_vertex)
            routing_table_before = copy.deepcopy(routing_table)
            self.player.find_route(routing_table, start_vertex, target_vertex)
            self.assertEqual(routing_table, routing_table_before, "Finding a route should not modify the routing table")

    ##################################################################################

    def test___dfs_find_route___fixed_routing_table___expected_outputs (self) -> None:

        """
        Category: normal use.
        This method tests the ``find_route(...)`` method on a manually created routing table.
        For a given routing table, source and target, there is a unique valid route.
        """

        # Routing table obtained with a traversal of the tree maze from vertex 4 (see the ``setUpClass(...)`` method)
        routing_table = {4: None, 1: 4, 3: 4, 7: 4, 0: 1, 2: 1, 6: 7, 8: 7, 5: 8}

        # The route should be exactly the expected one
        self.assertEqual(self.player.find_route(routing_table, 4, 3), [4, 3], "Wrong route from vertex 4 to vertex 3")
        self.assertEqual(self.player.find_route(routing_table, 4, 2), [4, 1, 2], "Wrong route from vertex 4 to vertex 2")
        self.assertEqual(self.player.find_route(routing_table, 4, 5), [4, 7, 8, 5], "Wrong route from vertex 4 to vertex 5")

    ##################################################################################

    def test___dfs_find_route___source_is_target___single_vertex_route (self) -> None:

        """
        Category: corner case.
        This method tests the ``find_route(...)`` method when the source and the target are the same vertex.
        The route should only contain that vertex, whether it is the root of the routing table or not.
        """

        # Routing table obtained with a traversal of the tree maze from vertex 4 (see the ``setUpClass(...)`` method)
        routing_table = {4: None, 1: 4, 3: 4, 7: 4, 0: 1, 2: 1, 6: 7, 8: 7, 5: 8}

        # The route should only contain the source
        self.assertEqual(self.player.find_route(routing_table, 4, 4), [4], "The route from the root to itself should only contain the root")
        self.assertEqual(self.player.find_route(routing_table, 7, 7), [7], "The route from a vertex to itself should only contain that vertex, even if it is not the root")

    ##################################################################################

    def test___dfs_find_route___source_is_not_root___partial_route (self) -> None:

        """
        Category: corner case.
        This method tests the ``find_route(...)`` method when the source is not the root of the routing table, but is an ancestor of the target.
        The route should stop at the source, and not go up to the root.
        """

        # Routing table obtained with a traversal of the tree maze from vertex 4 (see the ``setUpClass(...)`` method)
        routing_table = {4: None, 1: 4, 3: 4, 7: 4, 0: 1, 2: 1, 6: 7, 8: 7, 5: 8}

        # The route should start at the source
        self.assertEqual(self.player.find_route(routing_table, 1, 2), [1, 2], "The route from vertex 1 to vertex 2 should start at vertex 1, not at the root")
        self.assertEqual(self.player.find_route(routing_table, 7, 5), [7, 8, 5], "The route from vertex 7 to vertex 5 should start at vertex 7, not at the root")

    ##################################################################################

    def test___dfs_find_route___source_not_in_routing_table___raises_error (self) -> None:

        """
        Category: error case.
        This method tests the ``find_route(...)`` method when the source is not in the routing table.
        Going up from the target, the root is reached without meeting the source, and its parent (None) is not in the routing table.
        """

        # Routing table obtained with a traversal of the tree maze from vertex 4 (see the ``setUpClass(...)`` method)
        routing_table = {4: None, 1: 4, 3: 4, 7: 4, 0: 1, 2: 1, 6: 7, 8: 7, 5: 8}

        # Vertex 9 is not in the routing table
        with self.assertRaises(KeyError, msg="Finding a route from a vertex that is not in the routing table should raise an error"):
            self.player.find_route(routing_table, 9, 5)

    ##################################################################################

    def test___dfs_find_route___target_not_in_routing_table___raises_error (self) -> None:

        """
        Category: error case.
        This method tests the ``find_route(...)`` method when the target is not in the routing table.
        This happens when the target was not reached by the traversal, e.g., in a disconnected maze.
        """

        # Routing table obtained with a traversal of the tree maze from vertex 4 (see the ``setUpClass(...)`` method)
        routing_table = {4: None, 1: 4, 3: 4, 7: 4, 0: 1, 2: 1, 6: 7, 8: 7, 5: 8}

        # Vertex 9 is not in the routing table
        with self.assertRaises(KeyError, msg="Finding a route to a vertex that is not in the routing table should raise an error"):
            self.player.find_route(routing_table, 4, 9)

    ##################################################################################

    def test___dfs_find_route___unexpected_arguments___raises_error (self) -> None:

        """
        Category: error case.
        This method tests the ``find_route(...)`` method with arguments of unexpected types.
        """

        # Routing table obtained with a traversal of the tree maze from vertex 4 (see the ``setUpClass(...)`` method)
        routing_table = {4: None, 1: 4, 3: 4, 7: 4, 0: 1, 2: 1, 6: 7, 8: 7, 5: 8}

        # None is not a routing table, and "5" is a string, not the integer 5 that is in the routing table
        with self.assertRaises(TypeError, msg="Finding a route in None should raise an error"):
            self.player.find_route(None, 4, 5)
        with self.assertRaises(KeyError, msg="Finding a route to a string should raise an error"):
            self.player.find_route(routing_table, 4, "5")

    ##################################################################################

    def test___dfs_find_route___invalid_routing_table___raises_error (self) -> None:

        """
        Category: error case.
        This method tests the ``find_route(...)`` method with a routing table that cannot be the output of a traversal.
        Here, a vertex has a parent that is not in the routing table.
        Note that a routing table with a cycle (e.g., ``{1: 2, 2: 1}``) would make the method loop forever, so we do not test that case.
        """

        # The parent of vertex 1 is vertex 5, which is not in the routing table
        with self.assertRaises(KeyError, msg="Finding a route with a parent that is not in the routing table should raise an error"):
            self.player.find_route({0: None, 1: 5}, 0, 1)

    ##################################################################################

    def test___dfs_find_route___source_not_ancestor_of_target___raises_error (self) -> None:

        """
        Category: error case.
        This method tests the ``find_route(...)`` method when the source is not an ancestor of the target in the routing table.
        In that case, there is no route to follow from the source to the target.
        """

        # Routing table obtained with a traversal of the tree maze from vertex 4 (see the ``setUpClass(...)`` method)
        routing_table = {4: None, 1: 4, 3: 4, 7: 4, 0: 1, 2: 1, 6: 7, 8: 7, 5: 8}

        # Vertex 3 is in another branch than vertex 5
        with self.assertRaises(KeyError, msg="Finding a route from a vertex that is not an ancestor of the target should raise an error"):
            self.player.find_route(routing_table, 3, 5)

##########################################################################################
######################################### SCRIPT #########################################
##########################################################################################

if __name__ == "__main__":

    # Run all tests
    unittest.main(verbosity=2)

##########################################################################################
##########################################################################################