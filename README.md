# Project Identity
**Project Name:** Hnefatafl (Viking Chess) AI Player  
**Project Type:** Desktop/Console Game Application with AI Opponent  
**Project Category:** Artificial Intelligence, Adversarial Search Algorithm  
**One-Sentence Purpose:** A two-player, asymmetric strategy game implementing the Alpha-Beta pruning algorithm to allow a human to play intelligently against a computer opponent.  
**Explanation:** This project brings the ancient Norse board game "Hnefatafl" to life as a digital application. The game involves a small defending force trying to help their King escape to the corners of the board, while a larger attacking army attempts to capture the King by surrounding him. The core of this application is its Artificial Intelligence engine, which evaluates thousands of potential future moves to make optimal decisions against a human player.  
**Problem Solved:** Fulfills the requirements for the CS361 Artificial Intelligence course project by providing a practical, interactive demonstration of adversarial search algorithms (specifically Alpha-Beta pruning) in an asymmetric zero-sum game environment.  
**Intended Users:** 
- Students and Developers: To learn and demonstrate AI search algorithms.
- Professors/Teaching Assistants: To grade the implementation of Alpha-Beta pruning, utility functions, and knowledge representation.
- Players: Anyone interested in playing a challenging game of Viking Chess against an AI.

---

# Executive Summary
The Hnefatafl AI Project is a digital adaptation of a classic asymmetric board game where two players have fundamentally different objectives. One player commands a small team of defenders attempting to escort their King to safety at the edge of the board, while the other commands a larger attacking force trying to capture the King. 

What makes this project special is not just the game itself, but the "brain" behind the computer opponent. Instead of relying on random moves or hardcoded rules, the computer looks ahead into the future. By using an advanced artificial intelligence technique called "Alpha-Beta Pruning," the computer simulates all possible moves it can make, all possible responses the human can make, and so on. It explores these future timelines to find the sequence of moves that gives it the best possible advantage, while ignoring (pruning) useless timelines to save time. 

For a non-developer, playing against this AI will feel like playing against a highly strategic human who can foresee the consequences of their actions several steps in advance. The game will feature a referee system (Game Controller) that enforces the rules, switches turns, and offers different difficulty levels (Easy, Medium, Hard) by adjusting exactly how many steps into the future the computer is allowed to look.

---

# Full Tech Stack
*(Note: As the project directory currently only contains the requirement PDF and no source code, this represents the proposed and required technology stack for implementation).*

- **Language:** **Python 3.x** (or optionally **Prolog**)
  - **What it does:** Serves as the primary programming language for the entire logic, state representation, and AI algorithms.
  - **Why it is used:** Python is highly expressive, easy to read, and excellent for rapid prototyping of search algorithms. The assignment explicitly restricts the language choices to Python or Prolog.
  - **Impact of removal:** The project would cease to exist.

- **Algorithm:** **Alpha-Beta Pruning**
  - **What it does:** An optimized search algorithm that drastically reduces the number of nodes evaluated by the minimax algorithm in its search tree.
  - **Why it is used:** It is a strict mandatory requirement from the assignment guidelines to power the computer's decision-making. No other algorithms are allowed.
  - **Impact of removal:** The computer opponent would lose its "intelligence," causing automatic failure of the project grading criteria.

- **UI Framework (Optional Bonus):** **Pygame** or **Tkinter** (If implemented in Python)
  - **What it does:** Renders a 2D graphical representation of the board and handles mouse click events for user interactions.
  - **Why it is used:** Provides a user-friendly way to play the game, satisfying the "GUI 1 Bonus mark" grading criteria.
  - **Impact of removal:** The game would have to be played strictly through a Command Line Interface (CLI), which is less intuitive but still functional.

---

# Project Architecture
*(Proposed Folder & File Structure based on best practices for this assignment)*

- `main.py`
  - **Role:** The entry point of the application.
  - **Function:** Initializes the game state, configures the difficulty level, and boots up either the CLI or GUI loop.
- `board.py`
  - **Role:** Knowledge and State Representation.
  - **Function:** Houses the `Board` class. Represents the 9x9 or 11x11 grid, tracking where every piece (Attacker, Defender, King) is currently located. It handles the raw manipulation of moving a piece from point A to B.
- `game_controller.py`
  - **Role:** The Referee and State Manager.
  - **Function:** Manages the turn-based system. It ensures players only move their own pieces, switches turns between Human and Computer, checks for custodial captures (sandwiching) after every move, and declares win/loss states.
- `ai_agent.py`
  - **Role:** The Computer Player.
  - **Function:** Contains the `alpha_beta_search()` function. When it's the computer's turn, it receives the current board state and depth limit, running the search tree to return the optimal move.
- `rules.py`
  - **Role:** Move Generation & Validation.
  - **Function:** Given a board state, this module calculates every single legal move a player can make. It enforces rules like "pieces move like a Rook," "cannot pass through other pieces," and "cannot stop on the Throne."
- `evaluator.py`
  - **Role:** The Heuristic Utility Function.
  - **Function:** Takes a board state and evaluates its "goodness" for the computer, returning a numeric score. This is used by the AI to judge whether a future timeline is winning or losing.

**Separation of Concerns:** 
The architecture strictly separates the physical board state (`board.py`) from the rules of the game (`rules.py`), the flow of the match (`game_controller.py`), and the intelligence of the opponent (`ai_agent.py`).

---

# Data Flow & Logic Flow
1. **Game Setup:** The application starts. `board.py` initializes a 2D array placing the King on the Throne, 12 defenders around him, and 24 attackers on the board edges.
2. **Turn Start (Human):** The `game_controller.py` prompts the human player. 
3. **Input & Validation:** The human selects a piece and a destination. `rules.py` verifies the move is a valid horizontal/vertical slide with no obstacles.
4. **State Mutation:** `board.py` updates the piece's coordinates. 
5. **Capture & Win Check:** `game_controller.py` checks if the new piece placement "sandwiches" an enemy piece. If so, the enemy piece is deleted. It then checks if the King has reached a corner (Defender wins) or is surrounded on 4 sides (Attacker wins).
6. **Turn Switch (Computer):** Turn passes to the AI.
7. **AI Thinking:** `ai_agent.py` clones the current board and begins Alpha-Beta pruning. It asks `rules.py` for all legal moves, simulates them, and recursively explores responses up to the defined depth.
8. **Evaluation:** At the maximum depth, `evaluator.py` scores the boards. The best score bubbles up to the top of the search tree.
9. **AI Execution:** The computer submits its optimal move, mutating the board, capturing pieces, and checking for wins. The cycle repeats from step 2.

---

# Core Features & Functionality

### 1. Human vs. Computer Play Mode
- **What it does:** Allows a human to sit at the computer and play a full match against the AI.
- **How it works:** The Game Controller halts execution to wait for standard input (or UI events) during the human's turn, but triggers an autonomous function call to the AI agent during the computer's turn.

### 2. Alpha-Beta Pruning Decision Engine
- **What it does:** Calculates the best possible move without evaluating useless paths.
- **How it works:** It uses two values, Alpha (best already explored option along path to the root for maximizer) and Beta (best already explored option for minimizer). If it finds a move worse than a previously examined move, it "prunes" (stops exploring) that branch entirely, saving massive amounts of computation time.

### 3. Custodial Capture (Sandwiching)
- **What it does:** Captures opponent pieces according to Viking Chess rules.
- **How it works:** After a piece moves to `(x, y)`, the system checks the adjacent squares `(x+1, y)`, `(x-1, y)`, `(x, y+1)`, `(x, y-1)`. If an enemy piece is adjacent, it checks the square immediately past the enemy. If that square contains an allied piece, a corner, or the King's Throne, the enemy piece is captured and removed from the 2D array.

### 4. Difficulty Levels (Depth Control)
- **What it does:** Allows the user to select Easy, Medium, or Hard difficulty.
- **How it works:** Modifies the `depth` parameter passed to the Alpha-Beta function. 
  - Easy: Depth 1 (Computer only looks at immediate next moves).
  - Medium: Depth 3 (Computer looks at its move, human's response, and its subsequent counter-move).
  - Hard: Depth 5 (Computer thinks 5 steps into the future).

---

# Key Code Concepts

### Asymmetric Zero-Sum Game
Hnefatafl is asymmetric. The Attackers win by capturing the King, the Defenders win by escaping the King. This requires a highly specialized **Utility Function**. Unlike Chess, where piece values are somewhat symmetrical, the AI must evaluate board states differently depending on whether it is playing as the Attacker or Defender. 

### Alpha-Beta Pruning over Minimax
Minimax was rejected (and incurs a penalty in grading) because Hnefatafl has a massive branching factor (pieces move like Rooks, generating dozens of valid moves per turn). Standard Minimax to Depth 5 would take minutes or hours to compute. Alpha-Beta Pruning was chosen because it cuts the search space mathematically down to a fraction of the time, allowing Depth 5 to complete in seconds.

### State Representation (Immutability in Search)
During the AI's "thinking" phase, it must simulate thousands of moves. The game must employ efficient board cloning or move undoing (backtracking) so that simulating future states doesn't corrupt the *actual* ongoing game board.

---

# Dependencies & Integrations
As per the constraints of a standard university AI project, the core logic requires **Zero** external integrations.
- **No databases:** State is held entirely in memory (RAM).
- **No internet/APIs:** Processing is done purely locally on the CPU.
- **Optional GUI:** `pygame` if the GUI bonus is attempted. If this dependency is missing, the code will fail to run unless a CLI fallback is written.

---

# Environment & Configuration
- **Prerequisites:** Python 3.8 or higher. 
- **Configuration:** No environment variables (`.env`) or secrets are required. The only configuration is user input at startup (selecting Team: Attacker/Defender, and Difficulty: Easy/Medium/Hard).
- **Production vs Dev:** There is no production server. The script is run locally. 

---

# How to Run the Project
*(Anticipated Instructions upon code completion)*
1. **Prerequisites:** Install Python 3.
2. **Unzip:** Extract the `ID1_ID2_ID3_Group.zip` file.
3. **Open Terminal:** Navigate to the extracted folder.
4. **Install Dependencies (if GUI used):** Run `pip install pygame`.
5. **Run:** Execute the command `python main.py`.
6. **Play:** Follow the on-screen prompts to select difficulty and make moves.

---

# Knowledge Prerequisites — What You Need to Know

### TIER 1 — Must know before touching this code:
- **Python Data Structures (2D Lists):** 
  - *What:* Arrays within arrays to create a grid.
  - *Why:* To represent the physical game board.
  - *Learn:* Python documentation on lists and matrices.
- **Hnefatafl Ruleset:** 
  - *What:* Rook-like movement, sandwich capturing, King's escape.
  - *Why:* You cannot write move validation without knowing how the game is legally played.
  - *Learn:* Provided YouTube video links in the project PDF.

### TIER 2 — Must understand to contribute effectively:
- **Minimax Algorithm:**
  - *What:* A recursive algorithm for choosing the next move in an n-player game.
  - *Why:* The foundation of adversarial AI.
  - *Learn:* CS361 lecture slides / "Artificial Intelligence: A Modern Approach".
- **Alpha-Beta Pruning:**
  - *What:* Adding upper and lower bounds to Minimax to skip branches.
  - *Why:* Mandatory grading requirement.
  - *Learn:* CS361 Lab drafts and course materials.

### TIER 3 — Advanced knowledge to master the project fully:
- **Heuristic Evaluation Design:**
  - *What:* Crafting mathematical formulas to score board states.
  - *Why:* An AI is only as smart as its evaluation function. You must quantify abstract concepts like "King safety" or "Attacker blockade".
  - *Learn:* Research papers on Tafl game AI or chess evaluation heuristics.
- **Move Ordering Optimization:**
  - *What:* Sorting generated moves so the "best looking" moves are evaluated first in the Alpha-Beta tree.
  - *Why:* Alpha-Beta pruning is exponentially faster if it searches good moves first.

---

# Potential Issues & Improvements
- **Performance Bottleneck (Python CPU Limits):** Python is an interpreted language and can be slow at deep recursion. Depth 5 Alpha-Beta might experience noticeable lag (seconds to minutes) depending on how efficiently move generation is coded.
- **Heuristic Bias:** If the utility function heavily favors capturing pieces, the AI might accidentally let the King escape because it was too distracted hunting soldiers.
- **Missing Features:** No network multiplayer, no save/load game functionality (out of scope for the assignment).

---

# Glossary
- **Hnefatafl:** The ancient Viking board game being simulated.
- **Asymmetric Game:** A game where players have different starting conditions, piece counts, and win objectives.
- **Custodial Capture (Sandwiching):** The act of capturing an enemy by flanking them on two opposite sides.
- **Throne:** The exact center tile of the board where the King begins the game.
- **Alpha-Beta Pruning:** An optimization algorithm that stops evaluating a sequence of moves when it proves it cannot be better than a previously evaluated sequence.
- **Utility Function:** A function that looks at a snapshot of the game board and returns a number representing how good that board is for the computer player.
- **Zero-Sum Game:** A competitive situation where one player's gain is exactly equal to the other player's loss.
