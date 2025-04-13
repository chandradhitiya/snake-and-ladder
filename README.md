# 🎲 Snake and Ladder Game

A classic Snake and Ladder board game implementation with both command-line and web interfaces using Python and Flask.

![Snake and Ladder Game](https://raw.githubusercontent.com/chandradhitiya/snake-and-ladder/main/static/img/screenshot.png)

## Features

- Classic Snake and Ladder gameplay
- Support for 2-4 players
- Two different interfaces:
  - Command-line interface (CLI)
  - Web-based interface using Flask
- Visually appealing web UI with responsive design
- Real-time game state updates

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/chandradhitiya/snake-and-ladder.git
   cd snake-and-ladder
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## How to Play

### Command-line Interface

1. Run the Python script:
   ```
   python snake_ladder_game.py
   ```

2. Follow the on-screen instructions:
   - Enter the number of players (2-4)
   - Enter names for each player
   - Take turns rolling the dice by pressing Enter
   - First player to reach square 100 exactly wins!

### Web Interface

1. Start the Flask web server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. From the web interface:
   - Click "Start New Game"
   - Enter the number of players and their names
   - Click "Roll Dice" on each player's turn
   - Watch as players move around the board
   - First to reach square 100 wins!

## Game Rules

1. Players take turns rolling a single die to move their token.
2. To start the game, a player must roll a 6.
3. The tokens move according to the number shown on the die.
4. If a player's token lands on the lower end of a ladder, the token moves up to the ladder's higher end.
5. If a player's token lands on the head of a snake, the token moves down to the tail of the snake.
6. The first player to reach exactly square 100 is the winner.
7. If the die roll would take a player beyond square 100, the player's token doesn't move and the turn passes to the next player.

## Project Structure

```
snake-and-ladder/
│
├── app.py                 # Flask web application
├── snake_ladder_game.py   # Core game logic and CLI version
├── requirements.txt       # Python dependencies
├── README.md              # This file
│
├── static/                # Static web assets
│   └── css/
│       └── style.css      # Web interface styling
│
└── templates/             # Flask HTML templates
    ├── index.html         # Home page
    ├── new_game.html      # Player setup page
    └── game.html          # Main game interface
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the classic Snake and Ladder board game
- Built with Flask framework for the web interface
- Created by [Chandradhitiya](https://github.com/chandradhitiya)