import pandas as pd
from tqdm import tqdm

from board import Board
from game import Game
from player import PlayerAB, PlayerMM, PlayerBFMM


def simulate_games(first_player_class, second_player_class):
    depths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    results = []
    for first_player_depth in tqdm(depths):
        for second_player_depth in depths:
            player_1 = first_player_class(first_player_depth, True)
            player_2 = second_player_class(second_player_depth, False)

            game = Game(Board(), player_1, player_2)
            winner, num_moves = game.simulateLocalGame()
            results.append({'first_player': player_1.__class__,
                            'second_player': player_2.__class__,
                            'winner': winner,
                            'num_moves': num_moves})

    return results


def run_game():
    player_1 = PlayerBFMM(3, True)
    player_2 = PlayerAB(3, False)

    game = Game(Board(), player_1, player_2)
    winner, num_moves = game.simulateLocalGame()
    print(winner, num_moves)


if __name__ == "__main__":
    run_game()

    # ## simulate for mm first
    # results = simulate_games(PlayerMM, PlayerAB)
    # print(results)
    # results_df = pd.DataFrame(results)
    #
    # results_df.to_csv('mm_first_results.csv')
    #
    # ## simulate for AB first
    # results = simulate_games(PlayerAB, PlayerMM)
    # print(results)
    # results_df = pd.DataFrame(results)
    # results_df.to_csv('ab_first_results.csv')
