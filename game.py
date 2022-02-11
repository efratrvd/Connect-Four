import datetime

from board import Board, GameResult
from player import Player


class Game:
    def __init__(self, start_board: Board, player1: Player, player2: Player):
        self.start_board = start_board
        self.player1 = player1
        self.player2 = player2

    ########################################################################
    #                     Simulate a Local Game
    ########################################################################

    def simulateLocalGame(self):
        board = Board(orig=self.start_board)
        is_player_1 = True
        game_result = board.isTerminal()
        player1_times = []
        player2_times = []
        while board.isTerminal() == GameResult.ONGOING:
            # make move
            time1 = datetime.datetime.now()
            move = self.player1.findMove(board) if is_player_1 else self.player2.findMove(board)
            move_time_sec = (datetime.datetime.now() - time1).total_seconds()
            player1_times.append(move_time_sec) if is_player_1 else player2_times.append(move_time_sec)
            board.makeMove(move)
            # determines if the game is over or not
            game_result = board.isTerminal()
            is_player_1 = not is_player_1

        return game_result, board.numMoves, player1_times, player2_times
