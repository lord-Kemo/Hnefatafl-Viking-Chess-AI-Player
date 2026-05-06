# -------- member 1 --------

import math
from board import (
    BOARD_SIZE, CORNERS,
    find_king, get_valid_moves, get_all_moves,
    make_move, check_winner,
)

DIFFICULTY = {
    "easy":   1,
    "medium": 3,
    "hard":   5,
}


def evaluate(grid):
    """Score the board: positive = good for attackers, negative = good for defenders."""
    winner = check_winner(grid)
    if winner == "attacker":
        return 10000
    if winner == "defender":
        return -10000

    score = 0
    attacker_count = 0
    defender_count = 0
    kr, kc = find_king(grid)

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if grid[r][c] == "A":
                attacker_count += 1
                # attacker encirclement — reward attackers close to king
                if kr is not None and kc is not None:
                    dist = abs(r - kr) + abs(c - kc)
                    if dist <= 2:
                        score += 3
            elif grid[r][c] == "D":
                defender_count += 1

    # piece-count advantage
    score += attacker_count * 2
    score -= defender_count * 2

    if kr is not None and kc is not None:
        # king distance to nearest corner — further = better for attackers
        min_dist = min(abs(kr - cr) + abs(kc - cc) for cr, cc in CORNERS)
        score += min_dist * 5

        # king mobility — more moves = better for defenders
        king_moves = len(get_valid_moves(grid, kr, kc))
        score -= king_moves * 2

    return score


def alpha_beta(grid, depth, alpha, beta, is_maximizing):
    """Alpha-beta pruning. Returns the best achievable score."""
    winner = check_winner(grid)
    if winner is not None:
        return evaluate(grid)
    if depth == 0:
        return evaluate(grid)

    if is_maximizing:
        best = -math.inf
        for fr, fc, tr, tc in get_all_moves(grid, "attacker"):
            child = make_move(grid, fr, fc, tr, tc)
            val = alpha_beta(child, depth - 1, alpha, beta, False)
            best = max(best, val)
            alpha = max(alpha, val)
            if beta <= alpha:
                break  # prune
        return best if best != -math.inf else evaluate(grid)
    else:
        best = math.inf
        for fr, fc, tr, tc in get_all_moves(grid, "defender"):
            child = make_move(grid, fr, fc, tr, tc)
            val = alpha_beta(child, depth - 1, alpha, beta, True)
            best = min(best, val)
            beta = min(beta, val)
            if beta <= alpha:
                break  # prune
        return best if best != math.inf else evaluate(grid)


def get_best_move(grid, side, depth):
    """Pick the best move for the given side using alpha-beta search."""
    best_move = None

    if side == "attacker":
        best_score = -math.inf
        for fr, fc, tr, tc in get_all_moves(grid, "attacker"):
            child = make_move(grid, fr, fc, tr, tc)
            score = alpha_beta(child, depth - 1, -math.inf, math.inf, False)
            if score > best_score:
                best_score = score
                best_move = (fr, fc, tr, tc)
    else:
        best_score = math.inf
        for fr, fc, tr, tc in get_all_moves(grid, "defender"):
            child = make_move(grid, fr, fc, tr, tc)
            score = alpha_beta(child, depth - 1, -math.inf, math.inf, True)
            if score < best_score:
                best_score = score
                best_move = (fr, fc, tr, tc)

    return best_move

# -------- member 1 --------
