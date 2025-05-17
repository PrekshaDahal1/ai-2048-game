import numpy as np
from game_2048 import Game2048

def heuristic_score(board):
    def count_empty(board):
        return np.sum(board == 0)

    def max_tile(board):
        return np.max(board)

    def monotonicity(board):
        totals = [0, 0, 0, 0]  # left-right, right-left, up-down, down-up
        for row in board:
            for i in range(len(row) - 1):
                if row[i] > row[i + 1]:
                    totals[0] += row[i] - row[i + 1]
                else:
                    totals[1] += row[i + 1] - row[i]
        for col in board.T:
            for i in range(len(col) - 1):
                if col[i] > col[i + 1]:
                    totals[2] += col[i] - col[i + 1]
                else:
                    totals[3] += col[i + 1] - col[i]
        return -min(totals[0], totals[1]) - min(totals[2], totals[3])

    def smoothness(board):
        smooth = 0
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i, j] != 0:
                    value = np.log2(board[i, j])
                    for direction in [(0, 1), (1, 0)]:
                        x, y = i + direction[0], j + direction[1]
                        if 0 <= x < board.shape[0] and 0 <= y < board.shape[1] and board[x, y] != 0:
                            target_value = np.log2(board[x, y])
                            smooth -= abs(value - target_value)
        return smooth

    empty_weight = 270
    max_tile_weight = 1000
    mono_weight = 47
    smooth_weight = 15

    empty = count_empty(board)
    max_t = max_tile(board)
    mono = monotonicity(board)
    smooth = smoothness(board)

    score = empty_weight * empty + max_tile_weight * np.log2(max_t) + mono_weight * mono + smooth_weight * smooth
    return score

def simulate_move(board, move, game_instance):
    game = Game2048()
    game.board = board.copy()
    moved = game.move(move)
    return game.board if moved else board

def expectimax(board, depth, player_turn, game_instance):
    if depth == 0 or not game_instance.can_move():
        return heuristic_score(board)

    if player_turn:
        max_score = float('-inf')
        for move in ['Up', 'Down', 'Left', 'Right']:
            new_board = simulate_move(board, move, game_instance)
            if np.array_equal(new_board, board):
                continue
            score = expectimax(new_board, depth - 1, False, game_instance)
            max_score = max(max_score, score)
        return max_score
    else:
        empty_cells = list(zip(*np.where(board == 0)))
        if not empty_cells:
            return heuristic_score(board)

        scores = []
        for cell in empty_cells:
            for tile_value, prob in [(2, 0.9), (4, 0.1)]:
                new_board = board.copy()
                new_board[cell] = tile_value
                score = expectimax(new_board, depth - 1, True, game_instance)
                scores.append(score * prob / len(empty_cells))
        return sum(scores)

def get_best_move(board, game_instance, max_depth=3):
    best_move = None
    best_score = float('-inf')
    for move in ['Up', 'Down', 'Left', 'Right']:
        new_board = simulate_move(board, move, game_instance)
        if np.array_equal(new_board, board):
            continue
        score = expectimax(new_board, max_depth - 1, False, game_instance)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move