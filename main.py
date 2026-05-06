# -------- member 3 --------

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
turn = "attacker"
game_over = False
difficulty = DIFFICULTY["medium"]
difficulty_selected = False


def on_click(event):
    global selected, valid_moves, turn, grid

    if game_over or turn == "attacker":
        return
    if grid is None:
        return

    col = (event.x - PAD) // CELL
    row = (event.y - PAD) // CELL
    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return

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

    # otherwise try to select a defender / king
    piece = grid[row][col]
    if piece in ("D", "K"):
        selected = (row, col)
        valid_moves = get_valid_moves(grid, row, col)
    else:
        selected = None
        valid_moves = []
    draw_board()


def ai_turn():
    global grid, turn
    if grid is None:
        return

    # keep GUI responsive: hard mode still uses depth 5, but with a time cap
    move = get_best_move(grid, "attacker", difficulty, time_limit_seconds=2.5)
    if move is None:
        end_game("defender")
        return

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


def end_game(winner):
    global game_over
    game_over = True
    if winner == "defender":
        status.config(text="You win!  The King escaped!")
    else:
        status.config(text="AI wins!  The King was captured!")


def new_game():
    global grid, selected, valid_moves, turn, game_over
    if not difficulty_selected:
        status.config(text="Select difficulty first")
        return
    grid = create_board()
    selected = None
    valid_moves = []
    turn = "attacker"
    game_over = False
    status.config(text="AI is thinking ...")
    draw_board()
    root.after(50, ai_turn)

# -------- member 3 --------


# -------- member 4 --------

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

root = tk.Tk()
root.title("Hnefatafl — Viking Chess")
root.resizable(False, False)

canvas_size = CELL * BOARD_SIZE + PAD * 2
canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="#000")
canvas.pack()

status = tk.Label(root, text="Select difficulty to start", font=("Arial", 13))
status.pack(pady=(4, 0))

btn_frame = tk.Frame(root)
btn_frame.pack(pady=6)


def set_difficulty(d, btn):
    global difficulty, difficulty_selected
    difficulty = d
    difficulty_selected = True
    for b in diff_buttons:
        b.config(relief=tk.RAISED)
    btn.config(relief=tk.SUNKEN)
    new_game()

diff_buttons = []
for label, key in [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]:
    depth = DIFFICULTY[key]
    b = tk.Button(btn_frame, text=label, width=8)
    b.config(command=lambda d=depth, b=b: set_difficulty(d, b))
    b.pack(side=tk.LEFT, padx=3)
    diff_buttons.append(b)

tk.Label(btn_frame, text="  ").pack(side=tk.LEFT)
new_btn = tk.Button(btn_frame, text="New Game", width=10, command=lambda: new_game())
new_btn.pack(side=tk.LEFT, padx=3)


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

            cx = x1 + CELL // 2
            cy = y1 + CELL // 2
            if (r, c) in CORNERS:
                canvas.create_text(cx, cy, text="X", fill="#ddd",
                                   font=("Arial", 14, "bold"))
            elif (r, c) == THRONE and grid[r][c] == " ":
                canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4,
                                   fill="#b8860b", outline="")

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

            if piece == "K":
                canvas.create_text(cx, cy, text="K",
                                   font=("Arial", 14, "bold"))


canvas.bind("<Button-1>", on_click)
root.mainloop()

# -------- member 4 --------
