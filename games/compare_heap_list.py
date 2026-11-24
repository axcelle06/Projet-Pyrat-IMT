#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
This script empirically compares the execution time and asymptotic complexity of Dijkstra's algorithm using a binary min-heap
(`DijkstraTraversal`) versus an unsorted list (`ListDijkstraTraversal`) on randomly generated PyRat mazes of increasing size.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import math
import time
import matplotlib.pyplot as plt

# PyRat imports
from pyrat import Maze, RandomMaze
from utils.traversal.dijkstra_traversal import DijkstraTraversal
from utils.traversal.list_dijkstra_traversal import ListDijkstraTraversal
from utils.traversal.traversal import Traversal

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def measure ( algo:    Traversal,
              maze:    Maze,
              start:   int,
              nb_runs: int = 10
            ) ->       float:

    """
    Measures the average execution time of a full maze traversal over multiple runs.

    Args:
        algo:    Traversal instance to benchmark.
        maze:    Maze on which the traversal is executed.
        start:   Starting vertex of the traversal.
        nb_runs: Number of repetitions used to compute the average time.

    Returns:
        Average execution duration in seconds.
    """

    # Measure total time over nb_runs executions
    t0 = time.perf_counter()
    for _ in range(nb_runs):
        algo.traversal(maze, start)
    return (time.perf_counter() - t0) / nb_runs

#####################################################################################################################################################

def log_slope ( x: list[int],
                y: list[float]
              ) -> float:

    """
    Computes the overall slope between the first and last points on a log-log scale.

    Args:
        x: List of input sizes (number of maze cells).
        y: List of corresponding average execution times.

    Returns:
        Estimated power-law exponent k such that y scales as O(x^k).
    """

    return (math.log(y[-1]) - math.log(y[0])) / (math.log(x[-1]) - math.log(x[0]))

#####################################################################################################################################################
###################################################################### SCRIPT #######################################################################
#####################################################################################################################################################

if __name__ == "__main__":

    # Experiment parameters
    sizes = [10, 20, 30, 50, 75, 100]
    nb_cells = [s * s for s in sizes]
    times_heap = []
    times_list = []

    # Instantiate both traversal implementations
    heap_algo = DijkstraTraversal()
    list_algo = ListDijkstraTraversal()

    # Benchmark on mazes of increasing size
    for size in sizes:
        maze = RandomMaze(width=size,
                          height=size,
                          wall_percentage=50.0,
                          mud_percentage=20.0,
                          mud_range=[4, 9],
                          random_seed=42)
        start = maze.get_vertices()[0]

        times_heap.append(measure(heap_algo, maze, start))
        times_list.append(measure(list_algo, maze, start))

        # Ensure both implementations compute identical shortest-path distances
        assert heap_algo.get_distances() == list_algo.get_distances()

    # Plot results on a log-log scale
    plt.loglog(nb_cells, times_heap, "o-", label=f"Tas min (pente = {log_slope(nb_cells, times_heap):.2f})")
    plt.loglog(nb_cells, times_list, "s-", label=f"Liste (pente = {log_slope(nb_cells, times_list):.2f})")
    plt.xlabel("Nombre de cases")
    plt.ylabel("Temps moyen (s)")
    plt.legend()
    plt.show()

#####################################################################################################################################################
#####################################################################################################################################################