# External imports
import tqdm.auto as tqdm
import matplotlib.pyplot as pyplot
import scipy.stats as scstats
import time
import numpy as np

# PyRat imports
from pyrat import Game, GameMode
from players.randoms.random1 import Random1
from players.randoms.random2 import Random2
from players.randoms.random3 import Random3
from players.randoms.random4 import Random4
from players.bfs import BFS
from players.dfs import DFS
from players.traversal_player import TraversalPlayer
from utils.traversal.bfs_traversal import BFSTraversal
from utils.traversal.dfs_traversal import DFSTraversal

#ia utilisée pour calculer le préprocessing time


# Determines how many games will be played for each player
nb_games = 1000

# Customize the game elements
game_config = {"mud_percentage": 0.0,
            "nb_cheese": 1,
            "game_mode": GameMode.SIMULATION}

# Run the games for each player class
# players = [Random1(), Random2(), Random3(), Random4(), BFS(), DFS()]
players = [TraversalPlayer(BFSTraversal(), name="Factorized BFS"), BFS() ]
preproc_times = {player.get_name(): [] for player in players}
results = {player.get_name(): [] for player in players}

for player in players:
    orig_preprocessing = player.preprocessing #on stock la méthode on l'appelle pas
    def timed_preprocessing(maze, game_state, _orig=orig_preprocessing, _name=player.get_name()):
        t0 = time.perf_counter()
        res = _orig(maze, game_state)
        preproc_times[_name].append(time.perf_counter() - t0)
        return res
    player.preprocessing = timed_preprocessing
    for seed in tqdm.tqdm(range(nb_games), desc=player.get_name()):

        # Make the game with given seed
        game = Game(random_seed=seed, **game_config)
        game.add_player(player)
        stats = game.start()
        # Store the number of turns needed
        results[player.get_name()].append(stats["turns"])
    player.preprocessing = orig_preprocessing #restauration de la méthode d'origine


fig, (ax1,ax2) = pyplot.subplots(1,2,figsize=(15,5))

# Visualization of cumulative curves of numbers of turns taken per program
max_turn = max([max(results[player]) for player in results])
for player in results:
    turns = [0] + sorted(results[player]) + [max_turn]
    games_completed_per_turn = [len([turn for turn in results[player] if turn <= t]) * 100.0 / nb_games for t in turns]
    ax1.plot(turns, games_completed_per_turn, label=player)
ax1.set_title("Comparison of turns needed to complete all %d games" % (nb_games))
ax1.set_xlabel("Turns per game")
ax1.set_ylabel("% of games completed")
ax1.set_xscale("log")
ax1.legend()

for player in preproc_times:
    times_ms = sorted(np.array(preproc_times[player]) * 1000)
    y = np.arange(1, len(times_ms) + 1) * 100.0 / nb_games
    mean_ms = np.mean(times_ms)
    ax2.plot(times_ms, y, label=f"{player} (moy: {mean_ms:.3f} ms)")
ax2.set_title(f"Comparison of preprocessing time ({nb_games} games)")
ax2.set_xlabel("Preprocessing time (ms)")
ax2.set_ylabel("% of games completed")
ax2.legend()

fig.tight_layout()
fig.savefig("turns_comparison.png")

# Formal statistics to check if these curves are statistically significant
for i, player_1 in enumerate(results):
    for j, player_2 in enumerate(results):
        if j > i:
            test_turns = scstats.mannwhitneyu(results[player_1], results[player_2], alternative="two-sided")
            print(f"Mann-Whitney U test (turns) '{player_1}' vs '{player_2}':", test_turns)

            # <--- AJOUT 4 : test statistique sur le temps de préprocessing
            test_preproc = scstats.mannwhitneyu(preproc_times[player_1], preproc_times[player_2], alternative="two-sided")
            print(f"Mann-Whitney U test (preprocessing) '{player_1}' vs '{player_2}':", test_preproc)