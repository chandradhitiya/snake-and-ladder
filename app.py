from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
import os
import json
from snake_ladder_game import SnakeAndLadderGame

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Game state storage
games = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new-game', methods=['GET', 'POST'])
def new_game():
    if request.method == 'POST':
        # Get player information
        player_count = int(request.form.get('player_count'))
        player_names = []
        
        for i in range(player_count):
            name = request.form.get(f'player_{i+1}')
            player_names.append(name)
        
        # Create a new game instance
        game_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        
        # Initialize game
        game = SnakeAndLadderGame()
        
        # Set player names
        for name in player_names:
            game.player_names.append(name)
            game.players[name] = 0
            
        games[game_id] = {
            'game': game,
            'current_player_idx': 0,
            'winner': None,
            'last_roll': None,
            'message': f"Game started! {game.player_names[0]}'s turn."
        }
        
        # Store game ID in session
        session['game_id'] = game_id
        
        return redirect(url_for('play_game'))
    
    return render_template('new_game.html')

@app.route('/play')
def play_game():
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return redirect(url_for('index'))
    
    game_data = games[game_id]
    game = game_data['game']
    
    # Prepare board data for rendering
    board_data = prepare_board_data(game)
    
    return render_template(
        'game.html',
        board_data=board_data,
        players=game.players,
        current_player=game.player_names[game_data['current_player_idx']],
        winner=game_data['winner'],
        last_roll=game_data['last_roll'],
        message=game_data['message']
    )

@app.route('/roll-dice', methods=['POST'])
def roll_dice():
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return redirect(url_for('index'))
    
    game_data = games[game_id]
    game = game_data['game']
    
    if game_data['winner']:
        return jsonify({'redirect': url_for('play_game')})
    
    current_player_idx = game_data['current_player_idx']
    current_player = game.player_names[current_player_idx]
    
    # Roll the dice
    dice_roll = game.roll_dice()
    game_data['last_roll'] = dice_roll
    
    message = f"{current_player} rolled a {dice_roll}."
    
    # First roll must be 6 to start
    if game.players[current_player] == 0 and dice_roll != 6:
        message += f" {current_player} needs to roll a 6 to start. Try again next turn!"
        game_data['message'] = message
    else:
        # If this is the first valid roll, set position to 1 (start)
        if game.players[current_player] == 0:
            message += f" {current_player} rolled a 6 and enters the game!"
            game.players[current_player] = 1
            # Move only the remaining 5 steps (1 was used to enter)
            new_position = game.move_player(current_player, dice_roll - 1)
        else:
            new_position = game.move_player(current_player, dice_roll)
        
        # Update message with move information
        message += f" {current_player} moved to position {new_position}."
        
        # Check if there was a snake or ladder
        if new_position != game.players[current_player]:
            if new_position > game.players[current_player]:
                message += f" Climbed a ladder to {game.players[current_player]}!"
            else:
                message += f" Bitten by a snake! Moved down to {game.players[current_player]}."
        
        # Check for winner
        if game.players[current_player] == 100:
            game_data['winner'] = current_player
            message += f" 🎉 {current_player} won the game! 🎉"
    
    game_data['message'] = message
    
    # Next player's turn
    game_data['current_player_idx'] = (current_player_idx + 1) % len(game.player_names)
    
    return jsonify({'redirect': url_for('play_game')})

def prepare_board_data(game):
    board_data = []
    
    # Create a 10x10 board
    for i in range(10):
        row = []
        for j in range(10):
            # Calculate cell number (snake and ladder board goes in a zigzag)
            row_num = 9 - i
            cell_num = row_num * 10 + (j + 1) if row_num % 2 == 0 else row_num * 10 + (10 - j)
            
            # Create cell data
            cell = {
                'number': cell_num,
                'players': [],
                'has_snake': cell_num in game.snakes,
                'has_ladder': cell_num in game.ladders,
                'snake_to': game.snakes.get(cell_num),
                'ladder_to': game.ladders.get(cell_num)
            }
            
            # Add players on this cell
            for player, position in game.players.items():
                if position == cell_num:
                    cell['players'].append(player)
            
            row.append(cell)
        board_data.append(row)
    
    return board_data

if __name__ == '__main__':
    app.run(debug=True)