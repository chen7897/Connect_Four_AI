
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
Diagonally - 
<p align="center">
  <img src="docs/reg_diagonal_win.png" alt="Home Screen" width="300">
</p>
<br> <br>
Or reversed diagonally - 
<p align="center">
  <img src="docs/reverse_diagonal_win.png" alt="Home Screen" width="300">
</p>
<br> <br>

each one of those sequences of dics will result in a victory and the end of the game.

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

