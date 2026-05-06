BOARD_SIZE = 11
CORNERS = [(0, 0), (0, 10), (10, 0), (10, 10)]
THRONE = (5, 5)


def create_board():
    grid = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    # 24 attackers on the four edges
    attacker_spots = [
        (0,3),(0,4),(0,5),(0,6),(0,7),(1,5),
        (10,3),(10,4),(10,5),(10,6),(10,7),(9,5),
        (3,0),(4,0),(5,0),(6,0),(7,0),(5,1),
        (3,10),(4,10),(5,10),(6,10),(7,10),(5,9),
    ]
    for r, c in attacker_spots:
        grid[r][c] = "A"

    # 12 defenders in a cross around the center
    defender_spots = [
        (3,5),(4,4),(4,5),(4,6),
        (5,3),(5,4),(5,6),(5,7),
        (6,4),(6,5),(6,6),(7,5),
    ]
    for r, c in defender_spots:
        grid[r][c] = "D"

    # king sits on the throne
    grid[5][5] = "K"
    return grid


def copy_board(grid):
    return [row[:] for row in grid]


def find_king(grid):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if grid[r][c] == "K":
                return r, c
    return None, None


def get_valid_moves(grid, row, col):
    """Pieces slide like rooks — any number of squares, no jumping."""
    piece = grid[row][col]
    if piece == " ":
        return []

    moves = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            if grid[r][c] != " ":
                break
            # only the king can land on corners
            if (r, c) in CORNERS and piece != "K":
                break
            # only the king can stop on the throne; others skip over it
            if (r, c) == THRONE and piece != "K":
                r += dr
                c += dc
                continue
            moves.append((r, c))
            r += dr
            c += dc
    return moves


def make_move(grid, fr, fc, tr, tc):
    """Returns a NEW grid with the move applied and captures resolved."""
    new_grid = copy_board(grid)
    new_grid[tr][tc] = new_grid[fr][fc]
    new_grid[fr][fc] = " "
    do_captures(new_grid, tr, tc)
    return new_grid


def do_captures(grid, row, col):
    """After a piece lands on (row,col), sandwich-capture adjacent enemies."""
    piece = grid[row][col]

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if not (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE):
            continue

        target = grid[nr][nc]
        if target == " " or target == "K":
            continue

        # is the neighbor an enemy?
        if piece == "A" and target != "D":
            continue
        if piece in ("D", "K") and target != "A":
            continue

        # check the square on the far side of the enemy
        br, bc = nr + dr, nc + dc
        if not (0 <= br < BOARD_SIZE and 0 <= bc < BOARD_SIZE):
            continue

        # corners and empty throne are "hostile" — they help sandwich
        if (br, bc) in CORNERS:
            grid[nr][nc] = " "
            continue
        if (br, bc) == THRONE and grid[br][bc] == " ":
            grid[nr][nc] = " "
            continue

        # a friendly piece completes the sandwich
        beyond = grid[br][bc]
        if piece == "A" and beyond == "A":
            grid[nr][nc] = " "
        elif piece in ("D", "K") and beyond in ("D", "K"):
            grid[nr][nc] = " "

    # king has special capture — must be surrounded on ALL 4 sides
    if piece == "A":
        check_king_capture(grid)


def check_king_capture(grid):
    kr, kc = find_king(grid)
    if kr is None:
        return

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = kr + dr, kc + dc
        # board edge does NOT count as surrounding
        if not (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE):
            return
        if grid[nr][nc] == "A":
            continue
        if (nr, nc) in CORNERS:
            continue
        if (nr, nc) == THRONE and grid[nr][nc] == " ":
            continue
        return  # something friendly or empty next to king — not captured

    grid[kr][kc] = " "


def check_winner(grid):
    kr, kc = find_king(grid)
    if kr is None:
        return "attacker"
    if (kr, kc) in CORNERS:
        return "defender"
    return None


def get_all_moves(grid, side):
    """Get every legal (from_r, from_c, to_r, to_c) for one side."""
    moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            p = grid[r][c]
            if side == "attacker" and p == "A":
                for mr, mc in get_valid_moves(grid, r, c):
                    moves.append((r, c, mr, mc))
            elif side == "defender" and p in ("D", "K"):
                for mr, mc in get_valid_moves(grid, r, c):
                    moves.append((r, c, mr, mc))
    return moves
