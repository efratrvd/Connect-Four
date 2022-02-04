import math

from more_itertools import first

from board import GameResult


class Player:
    def __init__(self, depthLimit, isPlayerOne):

        self.isPlayerOne = isPlayerOne
        self.depthLimit = depthLimit
        self.two_streak = 99
        self.three_streak = 999
        self.four_streak = 99999

    # Returns a heuristic for the board position
    # Good positions for 0 pieces are positive and good positions for 1 pieces
    # are be negative
    def heuristic(self, board):
        heur = 0
        state = board.board
        for i in range(0, board.WIDTH):
            for j in range(0, board.HEIGHT):
                # check horizontal streaks
                try:
                    # add player one streak scores to heur
                    if state[i][j] == state[i + 1][j] == 0:
                        heur += self.two_streak
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == 0:
                        heur += self.three_streak
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == state[i + 3][j] == 0:
                        heur += self.four_streak

                    # subtract player two streak score to heur
                    if state[i][j] == state[i + 1][j] == 1:
                        heur -= self.two_streak
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == 1:
                        heur -= self.three_streak
                    if state[i][j] == state[i + 1][j] == state[i + 2][j] == state[i + 3][j] == 1:
                        heur -= self.four_streak
                except IndexError:
                    pass

                # check vertical streaks
                try:
                    # add player one vertical streaks to heur
                    if state[i][j] == state[i][j + 1] == 0:
                        heur += self.two_streak
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == 0:
                        heur += self.three_streak
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == state[i][j + 3] == 0:
                        heur += self.four_streak

                    # subtract player two streaks from heur
                    if state[i][j] == state[i][j + 1] == 1:
                        heur -= self.two_streak
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == 1:
                        heur -= self.three_streak
                    if state[i][j] == state[i][j + 1] == state[i][j + 2] == state[i][j + 3] == 1:
                        heur -= self.four_streak
                except IndexError:
                    pass

                # check positive diagonal streaks
                try:
                    # add player one streaks to heur
                    if not j + 3 > board.HEIGHT and state[i][j] == state[i + 1][j + 1] == 0:
                        heur += self.two_streak
                    if not j + 3 > board.HEIGHT and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == 0:
                        heur += self.three_streak
                    if not j + 3 > board.HEIGHT and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] \
                            == state[i + 3][j + 3] == 0:
                        heur += self.four_streak

                    # add player two streaks to heur
                    if not j + 3 > board.HEIGHT and state[i][j] == state[i + 1][j + 1] == 1:
                        heur -= self.two_streak
                    if not j + 3 > board.HEIGHT and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == 1:
                        heur -= self.three_streak
                    if not j + 3 > board.HEIGHT and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] \
                            == state[i + 3][j + 3] == 1:
                        heur -= self.four_streak
                except IndexError:
                    pass

                # check negative diagonal streaks
                try:
                    # add  player one streaks
                    if not j - 3 < 0 and state[i][j] == state[i + 1][j - 1] == 0:
                        heur += self.two_streak
                    if not j - 3 < 0 and state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] == 0:
                        heur += self.three_streak
                    if not j - 3 < 0 and state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] \
                            == state[i + 3][j - 3] == 0:
                        heur += self.four_streak

                    # subtract player two streaks
                    if not j - 3 < 0 and state[i][j] == state[i + 1][j - 1] == 1:
                        heur -= self.two_streak
                    if not j - 3 < 0 and state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] == 1:
                        heur -= self.three_streak
                    if not j - 3 < 0 and state[i][j] == state[i + 1][j - 1] == state[i + 2][j - 2] \
                            == state[i + 3][j - 3] == 1:
                        heur -= self.four_streak
                except IndexError:
                    pass
        return heur


class PlayerMM(Player):
    def __init__(self, depthLimit, isPlayerOne):
        super().__init__(depthLimit, isPlayerOne)

    # returns the optimal column to move in by implementing the MiniMax algorithm
    def findMove(self, board):
        score, move = self.miniMax(board, self.depthLimit, self.isPlayerOne)
        # print(self.isPlayerOne, "move made", move)
        return move

    # findMove helper function using miniMax algorithm
    def miniMax(self, board, depth, player):
        if board.isTerminal() == GameResult.TIE:
            return -math.inf if player else math.inf, -1
        elif depth == 0:
            return self.heuristic(board), -1

        if player:
            best_score = -math.inf
            shouldReplace = lambda x: x > best_score
        else:
            best_score = math.inf
            shouldReplace = lambda x: x < best_score

        best_move = -1
        children = board.children()
        for child in children:
            move, childboard = child
            temp_best_score = self.miniMax(childboard, depth - 1, not player)[0]
            if shouldReplace(temp_best_score):
                best_score = temp_best_score
                best_move = move
        return best_score, best_move


class PlayerAB(Player):
    def __init__(self, depthLimit, isPlayerOne):
        super().__init__(depthLimit, isPlayerOne)

    # returns the optimal column to move in by implementing the Alpha-Beta algorithm
    def findMove(self, board):
        score, move = self.alphaBeta(board, self.depthLimit, self.isPlayerOne, -math.inf, math.inf)
        return move

    # findMove helper function, utilizing alpha-beta pruning within the minimax algorithm
    def alphaBeta(self, board, depth, player, alpha, beta):
        if board.isTerminal() == GameResult.TIE:
            return -math.inf if player else math.inf, -1
        elif depth == 0:
            return self.heuristic(board), -1

        if player:
            bestScore = -math.inf
            shouldReplace = lambda x: x > bestScore
        else:
            bestScore = math.inf
            shouldReplace = lambda x: x < bestScore

        bestMove = -1

        children = board.children()
        for child in children:
            move, childboard = child
            temp = self.alphaBeta(childboard, depth - 1, not player, alpha, beta)[0]
            if shouldReplace(temp):
                bestScore = temp
                bestMove = move
            if player:
                alpha = max(alpha, temp)
            else:
                beta = min(beta, temp)
            if alpha >= beta:
                break
        return bestScore, bestMove


class ManualPlayer(Player):
    def findMove(self, board):
        opts = " "
        for c in range(board.WIDTH):
            opts += " " + (str(c + 1) if len(board.board[c]) < 6 else ' ') + "  "
        print(opts)

        col = input("Place an " + ('O' if self.isPlayerOne else 'X') + " in column: ")
        col = int(col) - 1
        return col


class PlayerBFMM(Player):
    def __init__(self, depthLimit, isPlayerOne):
        super().__init__(depthLimit, isPlayerOne)

    # returns the optimal column to move in by implementing the Best-First MiniMax algorithm
    def findMove(self, board):
        play_function = self.bf_max if self.isPlayerOne else self.bf_min
        score, move, _ = play_function(board, self.depthLimit, -math.inf, math.inf)
        print(self.isPlayerOne, "move made", move)
        return move

    def _replace_value(self, children, value, move, best_child):
        for i, (_, child) in enumerate(children):
            child_move, _ = child
            if move == child_move:
                children[i] = (value, best_child)
                break

    def bf_max(self, board, depth, alpha, beta):
        # case - the next node to expand is not on this principle branch
        # print('getting_children - max')
        is_max_depth = False
        children = board.children()
        children_values = []
        for child in children:
            move, child_board = child
            value = self.heuristic(child_board)
            if value > beta:
                return value, move, False
            children_values.append(value)

        if board.isTerminal() == GameResult.TIE:
            return -math.inf, -1, True
        elif depth == 0:
            return self.heuristic(board), -1, True

        if len(children) == 1:
            children.append(None)
            children_values.append(-math.inf)

        # print('got children values - max')
        sorted_children = sorted(zip(children_values, children), key=lambda t: t[0], reverse=True)
        best_score, best_child = first(sorted_children, default=(-math.inf, -1))
        while alpha <= best_score and best_score <= beta:
            previous_move, child_board = best_child
            second_best_value, _ = sorted_children[1]
            value, move, is_max_depth = self.bf_min(child_board, depth - 1, max(alpha, second_best_value), beta)

            self._replace_value(sorted_children, value, previous_move, best_child)
            sorted_children = sorted(sorted_children, key=lambda t: t[0], reverse=True)
            best_score, best_child = first(sorted_children, default=(-math.inf, -1))
            if is_max_depth:
                break

        best_move, _ = best_child

        return best_score, best_move, is_max_depth

    def bf_min(self, board, depth, alpha, beta):
        is_max_depth = False
        # print('getting_children - min')
        children = board.children()
        children_values = []
        for child in children:
            move, child_board = child
            value = self.heuristic(child_board)
            if value < alpha:
                return value, move, False
            children_values.append(value)

        if board.isTerminal() == GameResult.TIE:
            return math.inf, -1, True
        elif depth == 0:
            return self.heuristic(board), -1, True

        if len(children) == 1:
            children.append(None)
            children_values.append(math.inf)

        # print('got children values - min')
        sorted_children = sorted(zip(children_values, children), key=lambda t: t[0])
        best_score, best_child = first(sorted_children, default=(math.inf, -1))
        while alpha <= best_score and best_score <= beta:
            previous_move, child_board = best_child
            second_best_value, _ = sorted_children[1]
            value, move, is_max_depth= self.bf_max(child_board, depth - 1, alpha, min(beta, second_best_value))

            self._replace_value(sorted_children, value, previous_move, best_child)
            sorted_children = sorted(sorted_children, key=lambda t: t[0])
            best_score, best_child = first(sorted_children, default=(math.inf, -1))
            if is_max_depth:
                break

        best_move, _ = best_child
        return best_score, best_move, is_max_depth
