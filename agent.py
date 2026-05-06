# -------- member 1 --------

import math
import time
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


def order_moves(grid, side, moves):
    """Try better moves first so alpha-beta cuts more branches."""
    scored = []
    for fr, fc, tr, tc in moves:
        child = make_move(grid, fr, fc, tr, tc)
        s = evaluate(child)
        # attackers maximize score, defenders minimize score
        if side == "attacker":
            scored.append((s, (fr, fc, tr, tc)))
        else:
            scored.append((-s, (fr, fc, tr, tc)))
    scored.sort(reverse=True)
    return [m for _, m in scored]


def alpha_beta(grid, depth, alpha, beta, is_maximizing, end_time=None):
    """Alpha-beta pruning. Returns the best achievable score."""
    if end_time is not None and time.time() >= end_time:
        return evaluate(grid)

    winner = check_winner(grid)
    if winner is not None:
        return evaluate(grid)
    if depth == 0:
        return evaluate(grid)

    if is_maximizing:
        best = -math.inf
        moves = get_all_moves(grid, "attacker")
        moves = order_moves(grid, "attacker", moves)
        for fr, fc, tr, tc in moves:
            if end_time is not None and time.time() >= end_time:
                break
            child = make_move(grid, fr, fc, tr, tc)
            val = alpha_beta(child, depth - 1, alpha, beta, False, end_time)
            best = max(best, val)
            alpha = max(alpha, val)
            if beta <= alpha:
                break  # prune
        return best if best != -math.inf else evaluate(grid)
    else:
        best = math.inf
        moves = get_all_moves(grid, "defender")
        moves = order_moves(grid, "defender", moves)
        for fr, fc, tr, tc in moves:
            if end_time is not None and time.time() >= end_time:
                break
            child = make_move(grid, fr, fc, tr, tc)
            val = alpha_beta(child, depth - 1, alpha, beta, True, end_time)
            best = min(best, val)
            beta = min(beta, val)
            if beta <= alpha:
                break  # prune
        return best if best != math.inf else evaluate(grid)


def get_best_move(grid, side, depth, time_limit_seconds=None):
    """Pick the best move for the given side using alpha-beta search."""
    best_move = None
    end_time = None
    if time_limit_seconds is not None:
        end_time = time.time() + time_limit_seconds

    # iterative deepening: keep best from last fully searched depth
    max_depth = depth
    for current_depth in range(1, max_depth + 1):
        if end_time is not None and time.time() >= end_time:
            break

        if side == "attacker":
            best_score = -math.inf
            moves = get_all_moves(grid, "attacker")
            moves = order_moves(grid, "attacker", moves)
            for fr, fc, tr, tc in moves:
                if end_time is not None and time.time() >= end_time:
                    break
                child = make_move(grid, fr, fc, tr, tc)
                score = alpha_beta(
                    child, current_depth - 1, -math.inf, math.inf, False, end_time
                )
                if score > best_score:
                    best_score = score
                    best_move = (fr, fc, tr, tc)
        else:
            best_score = math.inf
            moves = get_all_moves(grid, "defender")
            moves = order_moves(grid, "defender", moves)
            for fr, fc, tr, tc in moves:
                if end_time is not None and time.time() >= end_time:
                    break
                child = make_move(grid, fr, fc, tr, tc)
                score = alpha_beta(
                    child, current_depth - 1, -math.inf, math.inf, True, end_time
                )
                if score < best_score:
                    best_score = score
                    best_move = (fr, fc, tr, tc)

    return best_move

# -------- member 1 --------
