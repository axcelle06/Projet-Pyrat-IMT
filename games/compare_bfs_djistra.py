# External imports
import statistics

# PyRat imports
from pyrat import Game, GameMode
from players.traversal_player import TraversalPlayer
from utils.traversal.bfs_traversal import BFSTraversal
from utils.traversal.dijkstra_traversal import DijkstraTraversal

if __name__ == "__main__":

    nb_games = 50
    mud_values = [0.0, 10.0, 20.0, 30.0, 50.0]

    for mud in mud_values:
        turns_bfs = []
        turns_dijkstra = []
        moves_bfs = []
        moves_dijkstra = []
        time_bfs = []
        time_dijkstra = []

        for seed in range(nb_games):
            config = {
                "maze_width": 21,
                "maze_height": 15,
                "nb_cheese": 1,
                "mud_percentage": mud,
                "mud_range": (4, 9),
                "random_seed": seed,
                "game_mode": GameMode.SIMULATION,
            }

            directions = ["north", "south", "east", "west"]
            # Partie BFS
            game = Game(**config)
            game.add_player(TraversalPlayer(BFSTraversal(), name="BFS"))
            stats = game.start()
            t_bfs = stats["turns"]
            m_bfs = sum(stats["players"]["BFS"]["actions"][d] for d in directions)
            cpu_bfs = stats["players"]["BFS"]["preprocessing_duration"]

            
            # Partie Dijkstra
            game = Game(**config)
            game.add_player(TraversalPlayer(DijkstraTraversal(), name="Dijkstra"))
            stats = game.start()
            t_dijk = stats["turns"]
            m_dijk = sum(stats["players"]["Dijkstra"]["actions"][d] for d in directions)
            cpu_dijk = stats["players"]["Dijkstra"]["preprocessing_duration"]

            # Vérification des propriétés sur chaque labyrinthe
            assert t_dijk <= t_bfs, f"Dijkstra plus lent que BFS sur seed {seed}"
            assert m_bfs <= m_dijk, f"BFS fait plus de cases que Dijkstra sur seed {seed}"

            turns_bfs.append(t_bfs)
            turns_dijkstra.append(t_dijk)
            moves_bfs.append(m_bfs)
            moves_dijkstra.append(m_dijk)
            time_bfs.append(cpu_bfs)
            time_dijkstra.append(cpu_dijk)

        print(f"Boue {mud}% :")
        print(f"  Tours  -> BFS : {statistics.mean(turns_bfs):.2f} | Dijkstra : {statistics.mean(turns_dijkstra):.2f}")
        print(f"  Cases  -> BFS : {statistics.mean(moves_bfs):.2f} | Dijkstra : {statistics.mean(moves_dijkstra):.2f}")
        print(f"  Temps  -> BFS : {statistics.mean(time_bfs)*1000:.2f} ms | Dijkstra : {statistics.mean(time_dijkstra)*1000:.2f} ms\n")