
# Connect Four AI
Chen Sabag
## Description
This is a Connect Four game with AI implementation. Players can compete against each other or against an AI. The project is built using Python and Pygame.

The game is played on a grid of 6x7 slots that start blank, and can be filled with red or yellow discs.
<p align="center">
  <img src="docs/empty_board.png" alt="Home Screen" width="300">
</p>

The goal is to connect 4 discs of the same color, before the second player manages to do so. <br> There are 4 different legal ways to do it: <br> <br>
Horizontally - 
<p align="center">
  <img src="docs/horizontal_win.png" alt="Home Screen" width="300">
</p>
<br> <br>
Vertically - 
<p align="center">
  <img src="docs/vertical_win.png" alt="Home Screen" width="300">
</p>
<br> <br>
Positive diagonally - 
<p align="center">
  <img src="docs/reg_diagonal_win.png" alt="Home Screen" width="300">
</p>
<br> <br>
Or negative diagonally - 
<p align="center">
  <img src="docs/reverse_diagonal_win.png" alt="Home Screen" width="300">
</p>
<br> <br>

Each one of those sequences of discs will result in a victory and the end of the game.
<br>
In my project i built an ai player to play the game against a player or another ai player, in order to check how well different ai models perform in this challenge.

## The Problem
My goal is to create a smart AI which will perform as a "very hard" difficulty.

## Development Journey: Improving the AI
To develop a robust AI for Connect Four, I went through several stages of improvement:
1. **Random Column Picker:**  
   Initially, the AI simply chose a random column to drop its disc. While functional, this method had no strategy and frequently resulted in poor performance.<br> <br>
2. **Best Move (Trivial):**  
   The next step was creating a `best_move_trivial` function. This function evaluated each column and selected the first column that would result in an immediate win. If no winning move was found, it would default to the first available column. While better than the random picker, this approach lacked foresight and often missed opportunities or fell into traps. <br><br>
 3. **Minimax Algorithm:**  
   To significantly enhance the AI, I implemented the Minimax algorithm, which evaluates game states by simulating all possible moves up to a specified depth. Its goal is to maximize the AI’s advantage while minimizing the opponent’s chances of success.  
   - **Scoring System:** A scoring mechanism was developed to evaluate board configurations, assigning higher scores to favorable setups (e.g., those closer to a win) and prioritizing blocking the opponent’s winning moves.
   - **Depth Limitation:** To manage computational costs, the algorithm was restricted to a fixed depth, balancing decision quality with performance.
   - **Recursive Search:** Minimax uses a recursive search to explore game states, alternating between maximizing the AI’s position and minimizing the opponent’s advantage. <br> <br>
   While Minimax significantly improved the AI’s gameplay, it faced a critical limitation: the exponential growth of computation time with increased depth. Though increasing the depth made the AI smarter by looking further ahead, it caused delays that disrupted the game's flow. This trade-off underscored the need for a more efficient approach, leading to the next enhancement: alpha-beta pruning. 
  4. **Minimax with Alpha-beta pruning:** <br>
    To optimize Minimax, I added Alpha-beta pruning, which improves performance by reducing the number of nodes the algorithm evaluates. Alpha-beta pruning eliminates branches in the game tree that don't need exploration, speeding up decision-making without compromising the AI's play quality. <br>
    - **Alpha:** The best score for the maximizing player (AI).<br>
    - **Beta:** The best score for the minimizing player (opponent) <br>
    This allows the AI to explore deeper moves faster, improving its efficiency while keeping decision quality intact. With Alpha-beta pruning, the AI can make quicker decisions by pruning unnecessary branches, allowing it to evaluate more moves in less time.
        

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/chen7897/Connect_Four_AI
   ```
2. Set up a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
Run the game with:
```
python game.py
```

## AI Algorithms
1. **Minimax**: A decision-making algorithm used for two-player games to find the optimal move.
2. **Genetic Algorithm**: An evolutionary algorithm to improve AI performance over time by simulating natural selection.

## Technologies Used
- Python
- Pygame
- NumPy
- Matplotlib (for visualizations)

