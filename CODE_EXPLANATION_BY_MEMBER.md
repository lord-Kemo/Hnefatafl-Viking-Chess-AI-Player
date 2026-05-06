# 🏛️ Hnefatafl AI Project — Code Explanation by Member

---

## 📋 Overview

This project implements a **Hnefatafl (Viking Chess) AI Player** with a graphical interface. The code is divided into four modules, each handled by one team member. Below is a **complete line-by-line breakdown** of what each person wrote and why.

---

# 👑 **MEMBER 1: Core AI Engine** (`agent.py`)

## **Mission**: Implement Alpha-Beta Pruning & AI Decision Making

**Graded Items:**
- ✅ Alpha-beta pruning algorithm (1 mark)
- ✅ Utility/heuristic function (1.5 marks)
- ✅ Difficulty levels (1 mark)
- **Total: 3.5 marks**

---

## **Section 1: Imports & Difficulty Setup**

```python
import math
from board import (
    BOARD_SIZE, CORNERS,
    find_king, get_valid_moves, get_all_moves,
    make_move, check_winner,
)
```

**What's happening?**
- Line 1: Import `math` module for infinity constants (`-math.inf`, `math.inf`)
- Lines 2-8: Import helper functions from `board.py` that we'll use for AI calculations:
  - `BOARD_SIZE`: Board dimensions (11x11)
  - `CORNERS`: List of corner positions where the King can escape
  - `find_king()`: Locate the King's position on the board
  - `get_valid_moves()`: Get legal moves for a piece
  - `get_all_moves()`: Get all legal moves for one player
  - `make_move()`: Apply a move to the board
  - `check_winner()`: Check if game is won

```python
DIFFICULTY = {
    "easy":   1,
    "medium": 3,
    "hard":   5,
}
```

**What's this?**
- Dictionary mapping difficulty levels to **search depths**
  - **Easy**: depth = 1 (AI thinks 1 move ahead)
  - **Medium**: depth = 3 (AI thinks 3 moves ahead)
  - **Hard**: depth = 5 (AI thinks 5 moves ahead)
- Deeper = smarter AI but slower calculations

---

## **Section 2: Utility/Heuristic Function**

```python
def evaluate(grid):
    """Score the board: positive = good for attackers, negative = good for defenders."""
```

**What's this function for?**
- Scores a board position as a single number
- **Positive score** = situation is good for Attackers (AI)
- **Negative score** = situation is good for Defenders (human)
- Alpha-Beta will use this to decide which moves are best

---

### **Part 2A: Check for Immediate Win/Loss**

```python
    winner = check_winner(grid)
    if winner == "attacker":
        return 10000
    if winner == "defender":
        return -10000
```

**What's happening?**
- If game is already over, return an extreme value:
  - **10000** = attackers won (very good for AI)
  - **-10000** = defenders won (very bad for AI)
- These extreme values ensure the AI prioritizes immediate wins/losses

---

### **Part 2B: Count Pieces & Find King**

```python
    score = 0
    attacker_count = 0
    defender_count = 0
    kr, kc = find_king(grid)
```

**What's this doing?**
- Initialize `score = 0` (neutral starting point)
- Create counters for attacker and defender pieces
- `kr, kc` = King's row and column position
- We'll use the King's position to evaluate mobility and danger

---

### **Part 2C: Score Attacker Pieces & Encirclement**

```python
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if grid[r][c] == "A":
                attacker_count += 1
                # attacker encirclement — reward attackers close to king
                if kr is not None and kc is not None:
                    dist = abs(r - kr) + abs(c - kc)
                    if dist <= 2:
                        score += 3
```

**What's happening?**
- Loop through every square on the board (11x11 = 121 squares)
- If we find an Attacker piece ("A"):
  - Increment `attacker_count`
  - Calculate Manhattan distance from this Attacker to the King
    - `dist = abs(r - kr) + abs(c - kc)` is the "block distance"
  - If the Attacker is within 2 squares of King: `score += 3`
    - **Why?** Attackers close to the King are helpful for encirclement
    - This encourages the AI to move pieces near the King

```python
            elif grid[r][c] == "D":
                defender_count += 1
```

**What's this?**
- If square has a Defender piece ("D"), just count it
- (We reward/punish defenders in the piece-count section below)

---

### **Part 2D: Score Piece Advantage**

```python
    # piece-count advantage
    score += attacker_count * 2
    score -= defender_count * 2
```

**What's happening?**
- **More Attackers = higher score**: Each attacker adds 2 points
- **More Defenders = lower score**: Each defender subtracts 2 points
- **Why?** Attackers winning means fewer defenders → AI prefers capturing defenders

---

### **Part 2E: King Distance to Corners**

```python
    if kr is not None and kc is not None:
        # king distance to nearest corner — further = better for attackers
        min_dist = min(abs(kr - cr) + abs(kc - cc) for cr, cc in CORNERS)
        score += min_dist * 5
```

**What's happening?**
- Check that King exists (hasn't been captured)
- Calculate distance from King to **nearest corner**:
  - Loop through all 4 corners: `(0,0), (0,10), (10,0), (10,10)`
  - For each corner, calculate Manhattan distance
  - Take the **minimum** distance (closest corner)
- **`score += min_dist * 5`**: The farther the King from corners, the higher the score
  - **Why?** Corners are Defender victory conditions
  - If King is far from escape, Attackers are winning → reward with points
  - If King is close to corner, Defenders are close to winning → low score

---

### **Part 2F: King Mobility**

```python
        # king mobility — more moves = better for defenders
        king_moves = len(get_valid_moves(grid, kr, kc))
        score -= king_moves * 2
```

**What's happening?**
- Count how many legal moves the King has: `len(get_valid_moves(...))`
- **`score -= king_moves * 2`**: Subtract 2 points per King move
  - **Why?** More moves for King = more escape options = good for Defenders = bad for Attackers
  - AI penalizes positions where King has many options
  - This encourages AI to trap the King

```python
    return score
```

**What's this?**
- Return the final score
- This single number represents how good the board position is for Attackers

---

## **Section 3: Alpha-Beta Pruning Algorithm**

```python
def alpha_beta(grid, depth, alpha, beta, is_maximizing):
    """Alpha-beta pruning. Returns the best achievable score."""
```

**What's this function for?**
- The **core AI brain** — searches the game tree and finds the best move
- Uses **Alpha-Beta Pruning** to cut out branches that don't matter
- Returns the best score achievable from this position

**Parameters:**
- `grid`: Current board state
- `depth`: How many moves ahead to search (1, 3, or 5 based on difficulty)
- `alpha`: Best score Maximizer (Attacker) can guarantee
- `beta`: Best score Minimizer (Defender) can guarantee
- `is_maximizing`: True if it's Attacker's turn, False if Defender's turn

---

### **Part 3A: Terminal States (Game Over)**

```python
    winner = check_winner(grid)
    if winner is not None:
        return evaluate(grid)
```

**What's happening?**
- Check if the game is already won/lost
- If yes, evaluate the board and stop searching (this branch is resolved)
- **Why?** No point searching deeper if game is finished

---

### **Part 3B: Depth Limit Reached**

```python
    if depth == 0:
        return evaluate(grid)
```

**What's happening?**
- If we've searched `depth` moves ahead, stop and evaluate
- **Why?** Searching forever is impossible; we set a limit and evaluate at that point
- Deeper = stronger AI but slower

---

### **Part 3C: Maximizing Player (Attacker)**

```python
    if is_maximizing:
        best = -math.inf
        for fr, fc, tr, tc in get_all_moves(grid, "attacker"):
```

**What's happening?**
- If it's Attacker's turn (Maximizing Player):
  - Initialize `best = -math.inf` (worst possible score)
  - Loop through every legal move for the Attacker: `(from_row, from_col, to_row, to_col)`

```python
            child = make_move(grid, fr, fc, tr, tc)
            val = alpha_beta(child, depth - 1, alpha, beta, False)
```

**What's this?**
- Apply the move to create a new board state: `child`
- Recursively call `alpha_beta` to evaluate the resulting position:
  - `depth - 1`: Look one move deeper
  - `False`: Next turn is Defender (Minimizing)
- Get the score (`val`) of this branch

```python
            best = max(best, val)
            alpha = max(alpha, val)
```

**What's happening?**
- Update `best`: Keep the highest score found so far
- Update `alpha`: Track the best score Attacker can guarantee

```python
            if beta <= alpha:
                break  # prune
```

**What's this? (The Pruning)**
- If `beta <= alpha`: Defender has a move elsewhere that's better than anything we can do here
  - **No point exploring this branch further**
  - `break` exits the loop
- This is the **magic of Alpha-Beta**: Skip branches that won't affect the final decision

```python
        return best if best != -math.inf else evaluate(grid)
```

**What's this?**
- Return the best score found
- If no moves exist (deadlock), evaluate current board

---

### **Part 3D: Minimizing Player (Defender)**

```python
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
```

**What's happening?**
- **Mirror of Maximizing Player**, but minimizes instead:
  - Start with `best = math.inf` (highest possible, trying to get lower)
  - Use `min()` instead of `max()`
  - Update `beta` instead of `alpha`
  - Recursive call passes `True` (Attacker's turn next)
- **Why the mirror?** Defender wants the **lowest** score (bad for Attackers)
- Pruning logic is identical

---

## **Section 4: Get Best Move**

```python
def get_best_move(grid, side, depth):
    """Pick the best move for the given side using alpha-beta search."""
    best_move = None
```

**What's this function for?**
- **High-level interface** to Alpha-Beta Pruning
- Takes a board and side ("attacker" or "defender")
- Returns the single best move: `(from_row, from_col, to_row, to_col)`

---

### **Part 4A: Attacker's Best Move**

```python
    if side == "attacker":
        best_score = -math.inf
        for fr, fc, tr, tc in get_all_moves(grid, "attacker"):
            child = make_move(grid, fr, fc, tr, tc)
            score = alpha_beta(child, depth - 1, -math.inf, math.inf, False)
            if score > best_score:
                best_score = score
                best_move = (fr, fc, tr, tc)
```

**What's happening?**
- For each legal Attacker move:
  1. Apply the move: `child`
  2. Evaluate with Alpha-Beta (Defender's turn next): `alpha_beta(..., False)`
  3. If this move scores higher than previous best:
     - Update `best_score`
     - Save this move as `best_move`
- After all moves, `best_move` is the Attacker's best option

---

### **Part 4B: Defender's Best Move**

```python
    else:
        best_score = math.inf
        for fr, fc, tr, tc in get_all_moves(grid, "defender"):
            child = make_move(grid, fr, fc, tr, tc)
            score = alpha_beta(child, depth - 1, -math.inf, math.inf, True)
            if score < best_score:
                best_score = score
                best_move = (fr, fc, tr, tc)

    return best_move
```

**What's happening?**
- Same as Attacker, but:
  - Start with `best_score = math.inf` (trying to minimize)
  - Use `<` instead of `>` (want lower scores)
  - Recursive call passes `True` (Attacker's turn next)
- Return the best move found

---

# 🔵 **MEMBER 2: Board & Moves Representation** (`board.py`)

## **Mission**: Represent Board State & Generate Legal Moves

**Graded Items:**
- ✅ Board and state representation (1.5 marks)
- ✅ Representing possible moves (1.5 marks)
- **Total: 3 marks**

---

## **Section 1: Constants**

```python
BOARD_SIZE = 11
CORNERS = [(0, 0), (0, 10), (10, 0), (10, 10)]
THRONE = (5, 5)
```

**What are these?**
- `BOARD_SIZE = 11`: The board is 11×11 (standard Hnefatafl)
- `CORNERS`: The four escape squares where Defenders can win
  - `(0, 0)` = top-left, `(0, 10)` = top-right, etc.
- `THRONE = (5, 5)`: The center square where the King starts
  - Only King can stop on Throne; others pass over it

---

## **Section 2: Create Initial Board**

```python
def create_board():
    grid = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]
```

**What's this?**
- Create an 11×11 2D list, filled with empty spaces `" "`
- `grid[row][col]` will store:
  - `" "` = empty square
  - `"A"` = Attacker piece
  - `"D"` = Defender piece
  - `"K"` = King

---

### **Part 2A: Place Attackers**

```python
    # 24 attackers on the four edges
    attacker_spots = [
        (0,3),(0,4),(0,5),(0,6),(0,7),(1,5),
        (10,3),(10,4),(10,5),(10,6),(10,7),(9,5),
        (3,0),(4,0),(5,0),(6,0),(7,0),(5,1),
        (3,10),(4,10),(5,10),(6,10),(7,10),(5,9),
    ]
    for r, c in attacker_spots:
        grid[r][c] = "A"
```

**What's happening?**
- Define 24 starting positions for Attackers (hardcoded in standard Hnefatafl)
  - 6 on top edge, 6 on bottom, 6 on left, 6 on right
  - Plus extras at key positions (e.g., `(1,5)` supports the top edge)
- Loop through each position and place an `"A"` piece

---

### **Part 2B: Place Defenders**

```python
    # 12 defenders in a cross around the center
    defender_spots = [
        (3,5),(4,4),(4,5),(4,6),
        (5,3),(5,4),(5,6),(5,7),
        (6,4),(6,5),(6,6),(7,5),
    ]
    for r, c in defender_spots:
        grid[r][c] = "D"
```

**What's happening?**
- Define 12 starting positions for Defenders in a cross pattern around the center
- Each position gets a `"D"` piece

---

### **Part 2C: Place King**

```python
    # king sits on the throne
    grid[5][5] = "K"
    return grid
```

**What's this?**
- Place the King `"K"` at the Throne `(5, 5)`
- Return the fully initialized board

---

## **Section 3: Copy Board**

```python
def copy_board(grid):
    return [row[:] for row in grid]
```

**What's this?**
- Create a **deep copy** of the board
- `row[:]` creates a copy of each row (not a reference)
- **Why?** When testing moves in Alpha-Beta, we don't want to modify the original board

---

## **Section 4: Find King**

```python
def find_king(grid):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if grid[r][c] == "K":
                return r, c
    return None, None
```

**What's this?**
- Loop through every square on the board
- When we find the King `"K"`, return its position `(r, c)`
- If King doesn't exist (captured), return `(None, None)`
- **Used by:** AI evaluation, capture checking, win condition checking

---

## **Section 5: Get Valid Moves for One Piece**

```python
def get_valid_moves(grid, row, col):
    """Pieces slide like rooks — any number of squares, no jumping."""
    piece = grid[row][col]
    if piece == " ":
        return []
```

**What's this?**
- Get all legal moves for the piece at `(row, col)`
- If square is empty, return empty list (no moves)

---

### **Part 5A: Slide in Four Directions**

```python
    moves = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
```

**What's this?**
- `moves` list will store valid destinations
- Loop through four directions:
  - `(-1, 0)` = up
  - `(1, 0)` = down
  - `(0, -1)` = left
  - `(0, 1)` = right

---

### **Part 5B: Slide Until Blocked**

```python
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            if grid[r][c] != " ":
                break
```

**What's happening?**
- Start one square in direction `(dr, dc)`
- Keep moving while:
  - `r` and `c` are within the board
  - Stop if we hit a piece (can't jump)

---

### **Part 5C: Corner Rule**

```python
            # only the king can land on corners
            if (r, c) in CORNERS and piece != "K":
                break
```

**What's this?**
- If this square is a corner and the piece is **not** the King:
  - `break` (can't land here)
- **Why?** Only King can escape to corners; other pieces bounce back

---

### **Part 5D: Throne Rule**

```python
            # only the king can stop on the throne; others skip over it
            if (r, c) == THRONE and piece != "K":
                r += dr
                c += dc
                continue
```

**What's this?**
- If this square is the Throne and piece is **not** King:
  - Skip this square: move to next square in this direction
  - `continue` goes back to the `while` condition
- **Why?** Other pieces can pass through Throne but not land on it
  - King can land on Throne

---

### **Part 5E: Add Valid Move**

```python
            moves.append((r, c))
            r += dr
            c += dc
    return moves
```

**What's this?**
- Add `(r, c)` to legal moves (this square is valid to land on)
- Move one square further: `r += dr`, `c += dc`
- Keep sliding (loop continues)
- After all directions explored, return the moves list

---

## **Section 6: Get All Moves for One Side**

```python
def get_all_moves(grid, side):
    """Get every legal (from_r, from_c, to_r, to_c) for one side."""
    moves = []
```

**What's this?**
- Get **every** legal move for one entire side (all Attackers or all Defenders)
- Returns list of moves as tuples: `(from_row, from_col, to_row, to_col)`

---

### **Part 6A: Loop Through Board**

```python
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            p = grid[r][c]
```

**What's this?**
- Loop through every square `(r, c)` on the board
- `p` is the piece at this square

---

### **Part 6B: Collect Attacker Moves**

```python
            if side == "attacker" and p == "A":
                for mr, mc in get_valid_moves(grid, r, c):
                    moves.append((r, c, mr, mc))
```

**What's happening?**
- If side is Attacker and this square has an Attacker piece:
  - Get all valid moves for this piece: `get_valid_moves(grid, r, c)`
  - For each valid destination `(mr, mc)`:
    - Add the move `(from_r, from_c, to_r, to_c)` to the list

---

### **Part 6C: Collect Defender Moves**

```python
            elif side == "defender" and p in ("D", "K"):
                for mr, mc in get_valid_moves(grid, r, c):
                    moves.append((r, c, mr, mc))
    return moves
```

**What's happening?**
- If side is Defender and this square has a Defender or King:
  - Get all valid moves and add them
  - **Why include King?** King is a Defender piece, same team
- Return the complete list of all moves for this side

---

# 🟢 **MEMBER 3: Game Controller & Board Display** (`main.py` + `board.py`)

## **Mission**: Game Loop, Move Application, Win/Loss Detection

**Graded Items:**
- ✅ Updating and printing board (1 mark)
- ✅ Player switching (0.5 marks)
- **Total: 1.5 marks**

---

## **Section 1: Apply Move & Captures** (in `board.py`)

```python
def make_move(grid, fr, fc, tr, tc):
    """Returns a NEW grid with the move applied and captures resolved."""
    new_grid = copy_board(grid)
    new_grid[tr][tc] = new_grid[fr][fc]
    new_grid[fr][fc] = " "
    do_captures(new_grid, tr, tc)
    return new_grid
```

**What's this function for?**
- Apply a move to the board and handle all captures
- Returns a **new board state** (doesn't modify original)

**Step by step:**
1. `new_grid = copy_board(grid)`: Create a copy to avoid changing original
2. `new_grid[tr][tc] = new_grid[fr][fc]`: Move piece to destination
3. `new_grid[fr][fc] = " "`: Empty the source square
4. `do_captures(new_grid, tr, tc)`: Handle any captures created by this move
5. Return the updated board

---

## **Section 2: Custodial Captures**

```python
def do_captures(grid, row, col):
    """After a piece lands on (row,col), sandwich-capture adjacent enemies."""
    piece = grid[row][col]
```

**What's this function for?**
- After a piece lands, check if it captured any enemies
- **Capture rule**: Enemy is captured if surrounded on both sides (sandwich)
- `piece` is the piece that just moved

---

### **Part 2A: Check Four Directions**

```python
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if not (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE):
            continue

        target = grid[nr][nc]
        if target == " " or target == "K":
            continue
```

**What's happening?**
- Check all four adjacent squares
- Skip if outside board or if empty/King (can't capture King here, special rules)

---

### **Part 2B: Check Enemy Type**

```python
        # is the neighbor an enemy?
        if piece == "A" and target != "D":
            continue
        if piece in ("D", "K") and target != "A":
            continue
```

**What's this?**
- If Attacker piece moved: can only capture Defenders
- If Defender/King moved: can only capture Attackers
- If not an enemy, `continue` (skip this direction)

---

### **Part 2C: Check Far Side**

```python
        # check the square on the far side of the enemy
        br, bc = nr + dr, nc + dc
        if not (0 <= br < BOARD_SIZE and 0 <= bc < BOARD_SIZE):
            continue
```

**What's this?**
- Look at the square **beyond** the neighbor (opposite side)
- If it's outside board, can't complete sandwich with board edge

---

### **Part 2D: Board Edge Captures**

```python
        # corners and empty throne are "hostile" — they help sandwich
        if (br, bc) in CORNERS:
            grid[nr][nc] = " "
            continue
        if (br, bc) == THRONE and grid[br][bc] == " ":
            grid[nr][nc] = " "
            continue
```

**What's happening?**
- **Special rule**: Corners and empty Throne act like enemy pieces
- If enemy is adjacent to corner/Throne: it's captured (sandwich complete)
- `grid[nr][nc] = " "`: Capture the enemy (remove it)

---

### **Part 2E: Friendly Piece Captures**

```python
        # a friendly piece completes the sandwich
        beyond = grid[br][bc]
        if piece == "A" and beyond == "A":
            grid[nr][nc] = " "
        elif piece in ("D", "K") and beyond in ("D", "K"):
            grid[nr][nc] = " "
```

**What's this?**
- If the square beyond is a **friendly** piece: enemy is sandwiched
- Capture the enemy (remove it)

---

### **Part 2F: King Capture**

```python
    # king has special capture — must be surrounded on ALL 4 sides
    if piece == "A":
        check_king_capture(grid)
```

**What's this?**
- After Attackers move, check if King was captured
- **Why only Attackers?** King is part of Defender team; only Attackers can capture it

---

## **Section 3: King Capture Rule**

```python
def check_king_capture(grid):
    """King must be surrounded on ALL 4 sides to be captured."""
    kr, kc = find_king(grid)
    if kr is None:
        return
```

**What's this?**
- Find the King's position
- If King doesn't exist (already captured), return

---

### **Part 3A: Check All Four Sides**

```python
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = kr + dr, kc + dc
        # board edge does NOT count as surrounding
        if not (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE):
            return
```

**What's happening?**
- Check all four sides of King
- **Crucial rule**: Board edges do NOT count as "surrounding"
  - If King is at board edge, it's not trapped
  - `return` (King is safe)

---

### **Part 3B: Check for Attackers**

```python
        if grid[nr][nc] == "A":
            continue
```

**What's this?**
- If this side has an Attacker: continue checking other sides
- We need Attackers on **all four** sides

---

### **Part 3C: Check for Escape Routes**

```python
        if (nr, nc) in CORNERS:
            continue
        if (nr, nc) == THRONE and grid[nr][nc] == " ":
            continue
        return  # something friendly or empty next to king — not captured
```

**What's this?**
- If this side has a corner or empty Throne: King has escape route
  - `continue` (not final proof King is surrounded)
- If this side has anything else (friendly piece or empty):
  - King is **not** surrounded
  - `return` (King is safe)

---

### **Part 3D: King Captured**

```python
    grid[kr][kc] = " "
```

**What's this?**
- If we got here, King has Attackers/corners/Throne on **all four** sides
- **King is captured!**
- Remove King from board: `grid[kr][kc] = " "`

---

## **Section 4: Check Winner**

```python
def check_winner(grid):
    """King on a corner -> defenders win. King missing -> attackers win."""
    kr, kc = find_king(grid)
    if kr is None:
        return "attacker"
```

**What's this?**
- Find King's position
- If King is missing (captured): **Attackers win**

---

### **Part 4B: King Reached Corner**

```python
    if (kr, kc) in CORNERS:
        return "defender"
    return None
```

**What's this?**
- If King is on a corner: **Defenders win** (escaped!)
- Otherwise: Game continues (`return None`)

---

## **Section 5: GUI/Game Loop** (in `main.py`)

```python
import tkinter as tk
from board import (
    BOARD_SIZE, CORNERS, THRONE,
    create_board, get_valid_moves, get_all_moves,
    make_move, check_winner,
)
from agent import get_best_move, DIFFICULTY

grid = None
selected = None
valid_moves = []
turn = "defender"
game_over = False
difficulty = DIFFICULTY["medium"]
```

**What's this?**
- Import Tkinter (GUI library) and board/agent functions
- Initialize **global game state**:
  - `grid`: Current board
  - `selected`: Currently selected piece (for UI)
  - `valid_moves`: Moves for selected piece
  - `turn`: Whose turn ("defender" or "attacker")
  - `game_over`: Has game ended?
  - `difficulty`: AI difficulty level (starts at medium)

---

### **Part 5A: Handle Mouse Click**

```python
def on_click(event):
    global selected, valid_moves, turn, grid

    if game_over or turn == "attacker":
        return
```

**What's this?**
- Handle mouse clicks on the board
- Exit if game is over or it's AI's turn

---

### **Part 5B: Convert Coordinates**

```python
    if grid is None:
        return

    col = (event.x - PAD) // CELL
    row = (event.y - PAD) // CELL
    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return
```

**What's this?**
- Convert pixel coordinates to board coordinates
- `PAD`: Padding around board (30 pixels)
- `CELL`: Size of each square (55 pixels)
- Exit if click is outside board

---

### **Part 5C: Execute Move**

```python
    # if a piece is selected and we clicked a valid destination — move
    if selected is not None and (row, col) in valid_moves:
        fr, fc = selected
        grid = make_move(grid, fr, fc, row, col)
        selected = None
        valid_moves = []
        draw_board()

        winner = check_winner(grid)
        if winner:
            end_game(winner)
            return

        turn = "attacker"
        status.config(text="AI is thinking ...")
        root.after(50, ai_turn)
        return
```

**What's happening?**
1. If a piece is selected AND we click a valid destination:
   - Apply the move: `make_move(...)`
   - Clear selection
   - Redraw board
2. Check if Defenders won
3. If not, switch to AI's turn: `turn = "attacker"`
4. `root.after(50, ai_turn)`: Schedule AI move 50ms later (let UI update)

---

### **Part 5D: Select Piece**

```python
    # otherwise try to select a defender / king
    piece = grid[row][col]
    if piece in ("D", "K"):
        selected = (row, col)
        valid_moves = get_valid_moves(grid, row, col)
    else:
        selected = None
        valid_moves = []
    draw_board()
```

**What's this?**
- If clicked square has a Defender or King:
  - Select it: `selected = (row, col)`
  - Get its valid moves: `valid_moves = get_valid_moves(...)`
- Otherwise: deselect
- Redraw board (to show selection/moves)

---

## **Section 6: AI Turn**

```python
def ai_turn():
    global grid, turn
    if grid is None:
        return

    move = get_best_move(grid, "attacker", difficulty)
    if move is None:
        end_game("defender")
        return
```

**What's this?**
- Get the AI's best move using Alpha-Beta
- If no moves available: Defenders win (Attackers are stuck)

---

### **Part 6B: Apply AI Move**

```python
    fr, fc, tr, tc = move
    grid = make_move(grid, fr, fc, tr, tc)
    draw_board()

    winner = check_winner(grid)
    if winner:
        end_game(winner)
        return

    if not get_all_moves(grid, "defender"):
        end_game("attacker")
        return

    turn = "defender"
    status.config(text="Your turn  (Defenders)")
```

**What's happening?**
1. Unpack move: `(from_r, from_c, to_r, to_c)`
2. Apply it: `make_move(...)`
3. Redraw board
4. Check if Attackers won
5. Check if Defenders have any moves (if not, Attackers win)
6. Switch to human's turn

---

## **Section 7: End Game**

```python
def end_game(winner):
    global game_over
    game_over = True
    if winner == "defender":
        status.config(text="You win!  The King escaped!")
    else:
        status.config(text="AI wins!  The King was captured!")
```

**What's this?**
- Mark game as over
- Display appropriate message

---

## **Section 8: New Game**

```python
def new_game():
    global grid, selected, valid_moves, turn, game_over
    grid = create_board()
    selected = None
    valid_moves = []
    turn = "defender"
    game_over = False
    status.config(text="Your turn  (Defenders)")
    draw_board()
```

**What's this?**
- Reset all game state
- Create fresh board
- Set human's turn
- Redraw everything

---

# 🟡 **MEMBER 4: GUI (Graphical User Interface)** (`main.py`)

## **Mission**: Visual Board, Clickable Pieces, Status Display (Bonus)

**Graded Item:**
- ✅ GUI (Bonus) (+1 mark)

---

## **Section 1: GUI Setup**

```python
CELL = 55
PAD = 30

LIGHT_SQ   = "#F5DEB3"
DARK_SQ    = "#D2B48C"
CORNER_SQ  = "#8B4513"
THRONE_SQ  = "#DAA520"
HIGHLIGHT  = "#90EE90"
ATK_COLOR  = "#333333"
DEF_COLOR  = "#EEEEEE"
KING_COLOR = "#FFD700"
SEL_COLOR  = "#FF4444"
```

**What's this?**
- `CELL = 55`: Each square is 55×55 pixels
- `PAD = 30`: 30-pixel border around board
- **Colors:**
  - `LIGHT_SQ`, `DARK_SQ`: Checkerboard squares
  - `CORNER_SQ`: Corner squares (brown)
  - `THRONE_SQ`: Throne square (gold)
  - `HIGHLIGHT`: Valid move highlight (green)
  - `ATK_COLOR`: Attacker pieces (dark)
  - `DEF_COLOR`: Defender pieces (light)
  - `KING_COLOR`: King (gold)
  - `SEL_COLOR`: Selected piece (red outline)

---

## **Section 2: Create Window & Canvas**

```python
root = tk.Tk()
root.title("Hnefatafl — Viking Chess")
root.resizable(False, False)

canvas_size = CELL * BOARD_SIZE + PAD * 2
canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="#000")
canvas.pack()
```

**What's this?**
- `root`: Main window
- Set title and prevent resizing
- `canvas_size`: Calculate canvas size based on board + padding
  - 55 × 11 + 30 × 2 = 605 + 60 = 665 pixels
- `canvas`: Drawing area (using Tkinter Canvas)

---

## **Section 3: Status Label**

```python
status = tk.Label(root, text="Your turn  (Defenders)", font=("Arial", 13))
status.pack(pady=(4, 0))
```

**What's this?**
- Display whose turn it is and game status
- Font size 13, Arial
- Packed below canvas with 4 pixels padding on top

---

## **Section 4: Difficulty Buttons**

```python
btn_frame = tk.Frame(root)
btn_frame.pack(pady=6)

def set_difficulty(d, btn):
    global difficulty
    difficulty = d
    for b in diff_buttons:
        b.config(relief=tk.RAISED)
    btn.config(relief=tk.SUNKEN)
```

**What's this?**
- `btn_frame`: Container for buttons
- `set_difficulty()`: When user clicks difficulty button:
  - Update global `difficulty` variable
  - Depress all buttons (relief=RAISED)
  - Press selected button (relief=SUNKEN)

---

### **Part 4A: Create Difficulty Buttons**

```python
diff_buttons = []
for label, key in [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]:
    depth = DIFFICULTY[key]
    b = tk.Button(btn_frame, text=label, width=8)
    b.config(command=lambda d=depth, b=b: set_difficulty(d, b))
    b.pack(side=tk.LEFT, padx=3)
    diff_buttons.append(b)
diff_buttons[1].config(relief=tk.SUNKEN)
```

**What's happening?**
- Create three buttons: Easy, Medium, Hard
- Each button calls `set_difficulty(depth, button)`
- Pack them horizontally with 3-pixel padding
- Start with Medium button pressed (index 1): `relief=tk.SUNKEN`

---

## **Section 5: New Game Button**

```python
tk.Label(btn_frame, text="  ").pack(side=tk.LEFT)
new_btn = tk.Button(btn_frame, text="New Game", width=10, command=lambda: new_game())
new_btn.pack(side=tk.LEFT, padx=3)
```

**What's this?**
- Add spacer label (just spaces)
- Create "New Game" button that calls `new_game()`
- Pack horizontally

---

## **Section 6: Draw Board (Main Rendering)**

```python
def draw_board():
    canvas.delete("all")
    if grid is None:
        return

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            x1 = PAD + c * CELL
            y1 = PAD + r * CELL
            x2 = x1 + CELL
            y2 = y1 + CELL
```

**What's this?**
- Erase previous drawing: `canvas.delete("all")`
- If no board yet: return
- Loop through all 121 squares
- Calculate pixel coordinates:
  - `x1, y1`: Top-left corner
  - `x2, y2`: Bottom-right corner

---

### **Part 6A: Draw Squares**

```python
            if (r, c) in CORNERS:
                color = CORNER_SQ
            elif (r, c) == THRONE:
                color = THRONE_SQ
            elif (r, c) in valid_moves:
                color = HIGHLIGHT
            elif (r + c) % 2 == 0:
                color = LIGHT_SQ
            else:
                color = DARK_SQ

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#222")
```

**What's this?**
- **Color logic:**
  - If corner: brown
  - Elif throne: gold
  - Elif in valid moves: green (highlighted)
  - Elif checkerboard light: tan
  - Else: dark tan
- `create_rectangle()`: Draw the square
- `outline="#222"`: Dark gray border

---

### **Part 6B: Mark Special Squares**

```python
            cx = x1 + CELL // 2
            cy = y1 + CELL // 2
            if (r, c) in CORNERS:
                canvas.create_text(cx, cy, text="X", fill="#ddd",
                                   font=("Arial", 14, "bold"))
            elif (r, c) == THRONE and grid[r][c] == " ":
                canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4,
                                   fill="#b8860b", outline="")
```

**What's this?**
- `cx, cy`: Center of square
- If corner: Draw "X" (big, bold, light)
- If throne is empty: Draw small gold circle (mark the throne)

---

### **Part 6C: Draw Pieces**

```python
            piece = grid[r][c]
            if piece == " ":
                continue

            rad = CELL // 2 - 6
            if piece == "A":
                fill = ATK_COLOR
            elif piece == "D":
                fill = DEF_COLOR
            else:
                fill = KING_COLOR

            outline = SEL_COLOR if selected == (r, c) else "#000"
            width = 3 if selected == (r, c) else 1
            canvas.create_oval(cx - rad, cy - rad, cx + rad, cy + rad,
                               fill=fill, outline=outline, width=width)
```

**What's happening?**
- Get piece at this square
- If empty: skip
- Calculate radius for piece circle: `CELL // 2 - 6` (slightly smaller than square)
- Determine color based on piece type
- If this piece is selected:
  - Red outline (thicker)
- Otherwise:
  - Black outline (thinner)
- Draw circle for piece

---

### **Part 6D: Draw King Label**

```python
            if piece == "K":
                canvas.create_text(cx, cy, text="K",
                                   font=("Arial", 14, "bold"))
```

**What's this?**
- If piece is King: Draw "K" on top of the gold circle
- Helps distinguish King from other pieces

---

## **Section 7: Event Binding & Run**

```python
canvas.bind("<Button-1>", on_click)
new_game()
root.mainloop()
```

**What's this?**
- `canvas.bind()`: Listen for left mouse click on canvas → call `on_click()`
- `new_game()`: Initialize first game
- `root.mainloop()`: Start GUI loop (wait for events)

---

# 📊 Summary by Grading

| Member | Component | Marks | Key Files |
|--------|-----------|-------|-----------|
| **1** | Alpha-Beta + Heuristic + Difficulty | 3.5 | `agent.py` |
| **2** | Board Representation + Move Generation | 3.0 | `board.py` (sections 1-6) |
| **3** | Game Controller + Display + Win Detection | 1.5 | `board.py` (sections 2-4) + `main.py` (sections 5-8) |
| **4** | GUI (Bonus) | +1.0 | `main.py` (sections 1-7) |
| **Total** | | **9.0** | |

---

# 🚀 How to Run

```bash
python main.py
```

- Click **Easy/Medium/Hard** to set AI difficulty
- Click pieces to select, then click highlighted squares to move
- Escape King to corner → **You win!**
- Capture King → **AI wins!**
- Click **New Game** to restart

---

# 🎓 Key Concepts Each Member Should Know

**Member 1 (AI):**
- Alpha-Beta pruning, minimax trees, game theory
- Heuristic design (board evaluation)
- Recursion and tree search

**Member 2 (Board):**
- 2D array representation
- Rook-like movement rules
- Iterator patterns, list comprehensions

**Member 3 (Controller):**
- Capture mechanics (sandwich rule)
- Game state management
- Conditional logic for win conditions

**Member 4 (GUI):**
- Tkinter basics (Canvas, buttons, labels)
- Pixel-to-board coordinate conversion
- Event handling (mouse clicks)
- Visualization and user feedback

