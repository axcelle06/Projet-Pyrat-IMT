# External imports
import tqdm.auto as tqdm
import matplotlib.pyplot as pyplot
import scipy.stats as scstats

# PyRat imports
from pyrat import Game, GameMode
from players.random1 import Random1
from players.random2 import Random2
from players.random3 import Random3
from players.random4 import Random4

# Determines how many games will be played for each player
nb_games = 1000

# Customize the game elements
game_config = {"mud_percentage": 0.0,
            "nb_cheese": 1,
            "game_mode": GameMode.SIMULATION}

# Run the games for each player class
players = [Random1(), Random2(), Random3(), Random4()]
results = {player.get_name(): [] for player in players}
for player in players:
    for seed in tqdm.tqdm(range(nb_games), desc=player.get_name()):

        # Make the game with given seed
        game = Game(random_seed=seed, **game_config)
        game.add_player(player)
        stats = game.start()

        # Store the number of turns needed
        results[player.get_name()].append(stats["turns"])

# Visualization of cumulative curves of numbers of turns taken per program
max_turn = max([max(results[player]) for player in results])
pyplot.figure(figsize=(10, 5))
for player in results:
    turns = [0] + sorted(results[player]) + [max_turn]
    games_completed_per_turn = [len([turn for turn in results[player] if turn <= t]) * 100.0 / nb_games for t in turns]
    pyplot.plot(turns, games_completed_per_turn, label=player)
pyplot.title("Comparison of turns needed to complete all %d games" % (nb_games))
pyplot.xlabel("Turns per game")
pyplot.ylabel("% of games completed")
pyplot.xscale("log")
pyplot.legend()
pyplot.savefig("turns_comparison.png")

# Formal statistics to check if these curves are statistically significant
for i, player_1 in enumerate(results):
    for j, player_2 in enumerate(results):
        if j > i:
            test_result = scstats.mannwhitneyu(results[player_1], results[player_2], alternative="two-sided")
            print("Mann-Whitney U test between turns of program '%s' and of program '%s':" % (player_1, player_2), test_result)