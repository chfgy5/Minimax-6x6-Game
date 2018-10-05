# Reference: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
import numpy as np
from math import inf as infinity
import random
import sys
import datetime

MM = 'o' # maximize player
NODE_COUNT = 0 # expanded node
opposit_symbol = { 'o':'x', 'x':'o'}

distance = np.zeros([6,6]) # disrance from the center to each position

# Calculate the distance for each position to the center
for i in range(distance.shape[0]):
    for j in range(distance.shape[1]):
        if not (i == distance.shape[0]/2 - 1 and j == distance.shape[1]/2 - 1):
            distance[i][j] = abs((distance.shape[0]/2 - 1) - i) + abs((distance.shape[1]/2 - 1) - j)

# Return the distance from previse array
def take_toward_middle(cell):
    return distance[cell[0]][cell[1]]

# Print the state to stdout
def print_board(state):
    for row in state:
        print('\n-------------------------------------')
        for cell in row:
            if cell:
                print('| ', cell, ' ', end='')
            else:
                print('|     ', end='')
        print('|', end='')
    print('\n-------------------------------------')

# Call to get heuristic value of the state
def heuristic(state):
    return evaluate_heuristic(state)

# Check the blank space at head and tail of 2-3 in a row
def blank_check(string, symbol, length, hs):
    # Count blank space and 2-3 in a row
    blank_count = sum([1 for chr in string if len(chr) == 0])
    symbol_count = string.count(symbol)
    
    # If the length is over the expected value then return zero - the combination isn't counted 
    if length != symbol_count:
        return 0
    else:
        # 3 in a row case
        if blank_count > 0 and length == 3:
            # Use dictionary to count the value for both oppoent and player
            h_dict = str(symbol.lower()) + '_' + str(length) + '_row_' + str(blank_count) + '_side'
            hs[h_dict][1] += 1
        # 2 in a row case
        elif blank_count > 0 and length == 2:
            # Use dictionary to count the value for both oppoent and player
            h_dict = str(symbol.lower()) + '_' + str(length) + '_row'
            hs[h_dict][1] += 1
        return blank_count

def evaluate_heuristic(board):
    # If the current turn is x, o is the opponent
    if MM == 'x':
        heuristics = {'x_3_row_2_side': [5, 0], 'o_3_row_2_side': [-10, 0], 'x_3_row_1_side': [3, 0], 'o_3_row_1_side': [-6, 0], 'x_2_row': [1, 0], 'o_2_row': [-1, 0]}
    # If the current turn is o, x is the opponent
    else:
        heuristics = {'o_3_row_2_side': [5, 0], 'x_3_row_2_side': [-10, 0], 'o_3_row_1_side': [3, 0], 'x_3_row_1_side': [-6, 0], 'o_2_row': [1, 0], 'x_2_row': [-1, 0]}
    
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            # Check for 3 in a row by column
            if j < board.shape[1] - 2 and board[i][j] and board[i][j] == board[i][j + 1] == board[i][j + 2]:
                temp = [board[i][j], board[i][j + 1], board[i][j + 2]]
                if 0 <= j - 1 < board.shape[1]: temp = [board[i][j - 1]] + temp
                if 0 <= j + 3 < board.shape[1]: temp = temp + [board[i][j + 3]]
                blank_check(temp, board[i][j], 3, heuristics)
            # Check for 2 in a row by column
            elif j < board.shape[1] - 1 and board[i][j] and board[i][j] == board[i][j + 1]:
                temp = [board[i][j], board[i][j + 1]]
                if 0 <= j - 1 < board.shape[1]: temp = [board[i][j - 1]] + temp
                if 0 <= j + 2 < board.shape[1]: temp = temp + [board[i][j + 2]]
                blank_check(temp, board[i][j], 2, heuristics)
            
            # Check for 3 in a row by row
            if i < board.shape[0] - 2 and board[i][j] and board[i][j] == board[i + 1][j] == board[i + 2][j]:
                temp = [board[i][j], board[i + 1][j], board[i + 2][j]]
                if 0 <= i - 1 < board.shape[0]: temp = [board[i - 1][j]] + temp
                if 0 <= i + 3 < board.shape[0]: temp = temp + [board[i + 3][j]]
                blank_check(temp, board[i][j], 3, heuristics)
            # Check for 2 in a row by row
            elif i < board.shape[0] - 1 and board[i][j] and board[i][j] == board[i + 1][j]:
                temp = [board[i][j], board[i + 1][j]]
                if 0 <= i - 1 < board.shape[0]: temp = [board[i - 1][j]] + temp
                if 0 <= i + 2 < board.shape[0]: temp = temp + [board[i + 2][j]]
                blank_check(temp, board[i][j], 2, heuristics)
            
            # Check for 3 in a row by diagonal
            if i < board.shape[0] - 2 and j < board.shape[1] - 2 and board[i][j] and board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2]:
                temp = [board[i][j], board[i + 1][j + 1], board[i + 2][j + 2]]
                if 0 <= i - 1 < board.shape[0] and 0 <= j - 1 < board.shape[1]: temp = [board[i - 1][j - 1]] + temp
                if 0 <= i + 3 < board.shape[0] and 0 <= j + 3 < board.shape[1]: temp = temp + [board[i + 3][j + 3]]
                blank_check(temp, board[i][j], 3, heuristics)
            # Check for 2 in a row by diagonal
            elif i < board.shape[0] - 1 and j < board.shape[1] - 1 and board[i][j] and board[i][j] == board[i + 1][j + 1]:
                temp = [board[i][j], board[i + 1][j + 1]]
                if 0 <= i - 1 < board.shape[0] and 0 <= j - 1 < board.shape[1]: temp = [board[i - 1][j - 1]] + temp
                if 0 <= i + 2 < board.shape[0] and 0 <= j + 2 < board.shape[1]: temp = temp + [board[i + 2][j + 2]]
                blank_check(temp, board[i][j], 2, heuristics)
            
            # Check for 3 in a row by diagonal
            if i < board.shape[0] - 2 and j > 2 and board[i][j] and board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2]:
                temp = [board[i][j], board[i + 1][j - 1], board[i + 2][j - 2]]
                if 0 <= i - 1 < board.shape[0] and 0 <= j + 1 < board.shape[1]: temp = [board[i - 1][j + 1]] + temp
                if 0 <= i + 3 < board.shape[0] and 0 <= j - 3 < board.shape[1]: temp = temp + [board[i + 3][j - 3]]
                blank_check(temp, board[i][j], 3, heuristics)
            # Check for 2 in a row by diagonal
            elif i < board.shape[0] - 1 and j > 1 and board[i][j] and board[i][j] == board[i + 1][j - 1]:
                temp = [board[i][j], board[i + 1][j - 1]]
                if 0 <= i - 1 < board.shape[0] and 0 <= j + 1 < board.shape[1]: temp = [board[i - 1][j + 1]] + temp
                if 0 <= i + 2 < board.shape[0] and 0 <= j - 2 < board.shape[1]: temp = temp + [board[i + 2][j - 2]]
                blank_check(temp, board[i][j], 2, heuristics)
    
    # Sum up the value and return as the heuristic value
    sum_h = sum([val[0] * val[1] for key, val in heuristics.items()])
    return sum_h


# Check 4 in a row, winner
def wins(board, symbol, print_winnner = False):
     for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            # 4 in a row by column
            if j < board.shape[1] - 3 and board[i][j] and symbol == board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3]:
                if print_winnner: print(symbol.upper()+" is the winner")
                return True
            # 4 in a row by row
            if i < board.shape[0] - 3 and board[i][j] and symbol == board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j]:
                if print_winnner: print(symbol.upper()+" is the winner")
                return True
            # 4 in a row by diagonal
            if i < board.shape[0] - 3 and j < board.shape[1] - 3 and symbol == board[i][j] and board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3]:
                if print_winnner: print(symbol.upper()+" is the winner")
                return True
            # 4 in a row by diagonal
            if i < board.shape[0] - 3 and j > 3 and board[i][j] and symbol == board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3]:
                if print_winnner: print(symbol.upper()+" is the winner")
                return True

# Check if any player already wins this gave
def game_over(state):
    return wins(state, 'o') or wins(state, 'x')


# Return the list of blank position of the state
def blank_cells(state):
    cells = []
    for i, row in enumerate(state):
        for j, cell in enumerate(row):
            # if the cell is blank add position i,j to the list
            if not cell: 
                cells.append([i, j])
    
    # Random the postion before minimax the state
    random.shuffle(cells)
    # Sort the position by using take_toward_middle,
    # returns the distance of its position to the center of the board, as the key 
    cells.sort(key=take_toward_middle)
    
    return cells

# Minimax function by using recursion
def minimax(state, depth, symbol):
    # Max node for the player
    if symbol == MM:
        best = [-1, -1, -infinity]
    # Min node for the opponent
    else:
        best = [-1, -1, +infinity]
    
    # This function will stop when depth is 0 or gave is over
    if depth == 0 or game_over(state):
        score = heuristic(state)
        return [-1, -1, score]
    
    # Get all possible state by searching for blank space
    for cell in blank_cells(state):
        
        # Temporary set the value in the board
        i, j = cell[0], cell[1]
        state[i][j] = symbol
        
        # Call itself for the next depth with opponent value of the current state
        score = minimax(state, depth - 1, opposit_symbol[symbol])
        
        # Revert the board back
        state[i][j] = ''
        score[0], score[1] = i, j
        
        # If the current depth is player
        if symbol == MM:
            # Max value
            if score[2] > best[2]:
                best = score 
        # If the current depth is opponent
        else:
            # Min value
            if score[2] < best[2]:
                best = score  
    return best

# Minimax function by using recursion, 
# alpha–beta pruning is a search algorithm that seeks to decrease the number of nodes
# that are evaluated by the minimax algorithm in its search tree.
def alphabeta_minimax(state, depth, alpha, beta, symbol):
    global NODE_COUNT
    NODE_COUNT += 1
    # This function will stop when depth is 0 or gave is over
    if depth == 0 or game_over(state):
        score = heuristic(state)
        return [-1, -1, score]
    
    # If the current depth is player
    if symbol == MM:
        best = [-1, -1, -infinity] # for max value
        for cell in blank_cells(state):
            i, j = cell[0], cell[1]
            state[i][j] = symbol
            
            # Call itself for the next depth with opponent value of the current state
            score = alphabeta_minimax(state, depth - 1, alpha, beta, opposit_symbol[symbol])
            state[i][j] = ''
            score[0], score[1] = i, j
            
            # Max value
            if score[2] > best[2]:
                best = score
            
            # Set new alpha to the biggest value
            alpha = max(alpha, best[2])
            
            # Stop this recusion stack if alpha (max value) is bigger than beta (min value)
            # because the min value will not affect the max value
            if alpha >= beta:
                break
        return best
    
    # If the current depth is opponent
    else:
        best = [-1, -1, +infinity] # for min value
        for cell in blank_cells(state):
            i, j = cell[0], cell[1]
            state[i][j] = symbol
            
            # Call itself for the next depth with opponent value of the current state
            score = alphabeta_minimax(state, depth - 1, alpha, beta, opposit_symbol[symbol])
            state[i][j] = ''
            score[0], score[1] = i, j
            
            # Min value
            if score[2] < best[2]:
                best = score
            
            # Set new beta to the smallest value
            beta = min(beta, best[2])
            
            # Stop this recusion stack if alpha (max value) is bigger than beta (min value)
            # because the min value will not affect the max value
            if alpha >= beta:
                break
        return best

# Move function is used to call minimax function to get the next move
def moves(state, symbol, desired_depth = 0, display_board = True, display_expanded_node = True):
    # Check blank spaces
    depth = len(blank_cells(state))
    
    # This function will stop when depth is 0 or gave is over
    if depth == 0 or game_over(state):
        return False
    
    # If depth is not paseed as an argument, the minimax will search till the deepest of the current state 
    if desired_depth > 0:
        depth = desired_depth
    
    if display_board: 
        print('\n\nAI turn [{}]'.format(symbol), end='')
        
    global NODE_COUNT
    NODE_COUNT = 0
    
    # Call minimax function to get the next move
    move = alphabeta_minimax(state, depth, -infinity, +infinity, symbol)
    
    # Set the move
    i, j = move[0], move[1]
    state[i][j] = symbol
    
    if display_board:
        print_board(state)
    if display_expanded_node:
        print("Total expanded nodes:", NODE_COUNT)
        
    return True

player_depth = { 'x':2, 'o':4 }
sum_total = list()
print('x is player 1')
print('o is player 2\n')

print('x places the first move at center of the board', end='')
playing_board = np.zeros([6,6], dtype=str)
playing_board[2][2] = 'x'
current_move = 'o'

print_board(playing_board)

# In 1 game, it can only be 36 moves
# This loop will stop when there is a winner or tie
for i in range(36):
    start = datetime.datetime.now()
    
    MM = current_move
    if not moves(playing_board, current_move, player_depth[current_move]):
        break
    stop = datetime.datetime.now()
    total = stop-start
    sum_total.append(round(total.total_seconds() * 1000, 2))
    print('Execution time:',round(total.total_seconds() * 1000, 2), 'ms')
    current_move = opposit_symbol[current_move]

print("\n")
if not game_over(playing_board) and not len(blank_cells(playing_board)):
    print("This game is tie")
else:
    wins(playing_board, opposit_symbol[MM], True)
    
print('Total Execution time:',round(sum(sum_total), 4), 'ms')


player_depth = { 'x':2, 'o':4 }
sum_total = list()
print('x is player 1')
print('o is player 2\n')

# Player 1, x, start first for 100 games
for game in range(1, 101):
    print("\nGame " + str(game), end="\n    ")
    sum_total = list()
    playing_board = np.zeros([6,6], dtype=str)
    current_move = 'x'
    # In 1 game, it can only be 36 moves
    # This loop will stop when there is a winner or tie
    for i in range(36):
        start = datetime.datetime.now()
        MM = current_move
        if not moves(playing_board, current_move, player_depth[current_move], False, False):
            break
        stop = datetime.datetime.now()
        total = stop-start
        sum_total.append(round(total.total_seconds() * 1000, 2))
        current_move = opposit_symbol[current_move]

    if not game_over(playing_board) and not len(blank_cells(playing_board)):
        print("This game is tie")
    else:
        wins(playing_board, opposit_symbol[MM], True)

    print('    Total Execution time:',round(sum(sum_total), 4), 'ms')


player_depth = { 'x':2, 'o':4 }
sum_total = list()
print('x is player 1')
print('o is player 2\n')

# Player 2, o, start first for 100 games
for game in range(1, 101):
    print("\nGame " + str(game), end="\n    ")
    sum_total = list()
    playing_board = np.zeros([6,6], dtype=str)
    current_move = 'o'
    
    # In 1 game, it can only be 36 moves
    # This loop will stop when there is a winner or tie
    for i in range(36):
        start = datetime.datetime.now()
        MM = current_move
        if not moves(playing_board, current_move, player_depth[current_move], False, False):
            break
        stop = datetime.datetime.now()
        total = stop-start
        sum_total.append(round(total.total_seconds() * 1000, 2))
        current_move = opposit_symbol[current_move]

    if not game_over(playing_board) and not len(blank_cells(playing_board)):
        print("This game is tie")
    else:
        wins(playing_board, opposit_symbol[MM], True)

    print('    Total Execution time:',round(sum(sum_total), 4), 'ms')
