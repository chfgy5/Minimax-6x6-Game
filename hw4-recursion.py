import numpy as np
from math import inf as infinity
import random
import sys
import datetime

MM = 'o' # Maximize player
NODE_COUNT = 0 # Expanded node
opposit_symbol = { 'o':'x', 'x':'o'}

distance = np.zeros([6,6])
for i in range(distance.shape[0]):
    for j in range(distance.shape[1]):
        if not (i == distance.shape[0]/2 - 1 and j == distance.shape[1]/2 - 1):
            distance[i][j] = abs((distance.shape[0]/2 - 1) - i) + abs((distance.shape[1]/2 - 1) - j)

def take_toward_middle(cell):
    return distance[cell[0]][cell[1]]

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

def heuristic(state):
    return evaluate_heuristic(state)

def blank_check(string, symbol, length, hs):
    blank_count = sum([1 for chr in string if len(chr) == 0])
    symbol_count = string.count(symbol)
    if length != symbol_count:
        return 0
    else:
        if blank_count > 0 and length == 3:
            h_dict = str(symbol.lower()) + '_' + str(length) + '_row_' + str(blank_count) + '_side'
            hs[h_dict][1] += 1
        elif blank_count > 0 and length == 2:
            h_dict = str(symbol.lower()) + '_' + str(length) + '_row'
            hs[h_dict][1] += 1
        return blank_count

def evaluate_heuristic(board):
    if MM == 'x':
        heuristics = {'x_3_row_2_side': [5, 0], 'o_3_row_2_side': [-10, 0], 'x_3_row_1_side': [3, 0], 'o_3_row_1_side': [-6, 0], 'x_2_row': [1, 0], 'o_2_row': [-1, 0]}
    else:
        heuristics = {'o_3_row_2_side': [5, 0], 'x_3_row_2_side': [-10, 0], 'o_3_row_1_side': [3, 0], 'x_3_row_1_side': [-6, 0], 'o_2_row': [1, 0], 'x_2_row': [-1, 0]}
        
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if j < board.shape[1] - 2 and board[i][j] and board[i][j] == board[i][j + 1] == board[i][j + 2]:
                temp = [board[i][j], board[i][j + 1], board[i][j + 2]]
                if 0 <= j - 1 < board.shape[1]: temp = [board[i][j - 1]] + temp
                if 0 <= j + 3 < board.shape[1]: temp = temp + [board[i][j + 3]]
                blank_check(temp, board[i][j], 3, heuristics)

            elif j < board.shape[1] - 1 and board[i][j] and board[i][j] == board[i][j + 1]:
                temp = [board[i][j], board[i][j + 1]]
                if 0 <= j - 1 < board.shape[1]: temp = [board[i][j - 1]] + temp
                if 0 <= j + 2 < board.shape[1]: temp = temp + [board[i][j + 2]]
                blank_check(temp, board[i][j], 2, heuristics)

            if i < board.shape[0] - 2 and board[i][j] and board[i][j] == board[i + 1][j] == board[i + 2][j]:
                temp = [board[i][j], board[i + 1][j], board[i + 2][j]]
                if 0 <= i - 1 < board.shape[0]: temp = [board[i - 1][j]] + temp
                if 0 <= i + 3 < board.shape[0]: temp = temp + [board[i + 3][j]]
                blank_check(temp, board[i][j], 3, heuristics)

            elif i < board.shape[0] - 1 and board[i][j] and board[i][j] == board[i + 1][j]:
                temp = [board[i][j], board[i + 1][j]]
                if 0 <= i - 1 < board.shape[0]: temp = [board[i - 1][j]] + temp
                if 0 <= i + 2 < board.shape[0]: temp = temp + [board[i + 2][j]]
                blank_check(temp, board[i][j], 2, heuristics)

            if i < board.shape[0] - 2 and j < board.shape[1] - 2 and board[i][j] and board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2]:
                temp = [board[i][j], board[i + 1][j + 1], board[i + 2][j + 2]]
                if 0 <= i - 1 < board.shape[0] and 0 <= j - 1 < board.shape[1]: temp = [board[i - 1][j - 1]] + temp
                if 0 <= i + 3 < board.shape[0] and 0 <= j + 3 < board.shape[1]: temp = temp + [board[i + 3][j + 3]]
                blank_check(temp, board[i][j], 3, heuristics)

            elif i < board.shape[0] - 1 and j < board.shape[1] - 1 and board[i][j] and board[i][j] == board[i + 1][j + 1]:
                temp = [board[i][j], board[i + 1][j + 1]]
                if 0 <= i - 1 < board.shape[0] and 0 <= j - 1 < board.shape[1]: temp = [board[i - 1][j - 1]] + temp
                if 0 <= i + 2 < board.shape[0] and 0 <= j + 2 < board.shape[1]: temp = temp + [board[i + 2][j + 2]]
                blank_check(temp, board[i][j], 2, heuristics)

            if i < board.shape[0] - 2 and j > 2 and board[i][j] and board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2]:
                temp = [board[i][j], board[i + 1][j - 1], board[i + 2][j - 2]]
                if 0 <= i - 1 < board.shape[0] and 0 <= j + 1 < board.shape[1]: temp = [board[i - 1][j + 1]] + temp
                if 0 <= i + 3 < board.shape[0] and 0 <= j - 3 < board.shape[1]: temp = temp + [board[i + 3][j - 3]]
                blank_check(temp, board[i][j], 3, heuristics)

            elif i < board.shape[0] - 1 and j > 1 and board[i][j] and board[i][j] == board[i + 1][j - 1]:
                temp = [board[i][j], board[i + 1][j - 1]]
                if 0 <= i - 1 < board.shape[0] and 0 <= j + 1 < board.shape[1]: temp = [board[i - 1][j + 1]] + temp
                if 0 <= i + 2 < board.shape[0] and 0 <= j - 2 < board.shape[1]: temp = temp + [board[i + 2][j - 2]]
                blank_check(temp, board[i][j], 2, heuristics)
    sum_h = sum([val[0] * val[1] for key, val in heuristics.items()])
    return sum_h


def wins(board, symbol, print_winnner = False):
     for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if j < board.shape[1] - 3 and board[i][j] and symbol == board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3]:
                if print_winnner: print("\n\n"+symbol.upper()+" is the winner")
                return True
            if i < board.shape[0] - 3 and board[i][j] and symbol == board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j]:
                if print_winnner: print("\n\n"+symbol.upper()+" is the winner")
                return True
            if i < board.shape[0] - 3 and j < board.shape[1] - 3 and symbol == board[i][j] and board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3]:
                if print_winnner: print("\n\n"+symbol.upper()+" is the winner")
                return True
            if i < board.shape[0] - 3 and j > 3 and board[i][j] and symbol == board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3]:
                if print_winnner: print("\n\n"+symbol.upper()+" is the winner")
                return True

def game_over(state):
    return wins(state, 'o') or wins(state, 'x')


def blank_cells(state):
    cells = []
    for i, row in enumerate(state):
        for j, cell in enumerate(row):
            if not cell: 
                cells.append([i, j])
    
    random.shuffle(cells)
    cells.sort(key=take_toward_middle)
    return cells

def minimax(state, depth, symbol):
    if symbol == MM:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = heuristic(state)
        return [-1, -1, score]

    for cell in blank_cells(state):
        i, j = cell[0], cell[1]
        state[i][j] = symbol
        score = minimax(state, depth - 1, opposit_symbol[symbol])
        state[i][j] = ''
        score[0], score[1] = i, j

        if symbol == MM:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best

def alphabeta_minimax(state, depth, alpha, beta, symbol):
    global NODE_COUNT
    NODE_COUNT += 1
    if depth == 0 or game_over(state):
        score = heuristic(state)
        return [-1, -1, score]
    
    if symbol == MM:
        best = [-1, -1, -infinity]
        for cell in blank_cells(state):
            i, j = cell[0], cell[1]
            state[i][j] = symbol
            
            score = alphabeta_minimax(state, depth - 1, alpha, beta, opposit_symbol[symbol])
            state[i][j] = ''
            score[0], score[1] = i, j
            if score[2] > best[2]:
                best = score
                
            alpha = max(alpha, best[2])
            if alpha >= beta:
                break
        return best
    else:
        best = [-1, -1, +infinity]
        for cell in blank_cells(state):
            i, j = cell[0], cell[1]
            state[i][j] = symbol
            
            score = alphabeta_minimax(state, depth - 1, alpha, beta, opposit_symbol[symbol])
            state[i][j] = ''
            score[0], score[1] = i, j
            if score[2] < best[2]:
                best = score
                
            beta = min(beta, best[2])
            if alpha >= beta:
                break
        return best

def moves(state, symbol, desired_depth = 0):
    player_depth = { 'x':4, 'o':2 }
    
    depth = len(blank_cells(state))
    if depth == 0 or game_over(state):
        return False
    if desired_depth > 0: depth = desired_depth
        
    print('\n\nAI turn [{}]'.format(symbol), end='')
    global NODE_COUNT
    NODE_COUNT = 0
    move = alphabeta_minimax(state, player_depth[symbol], -infinity, +infinity, symbol)
    i, j = move[0], move[1]
    state[i][j] = symbol
    print_board(state)
    print("Total expanded nodes:", NODE_COUNT)
    return True

sum_total = list()
playing_board = np.zeros([6,6], dtype=str)
playing_board[2][2] = 'x'
print_board(playing_board)
current_move = 'o'

for i in range(36):
    start = datetime.datetime.now()
    MM = current_move
    if not moves(playing_board, current_move):
        break
    stop = datetime.datetime.now()
    total = stop-start
    sum_total.append(round(total.total_seconds() * 1000, 2))
    print('Execution time:',round(total.total_seconds() * 1000, 2), 'ms')
    current_move = opposit_symbol[current_move]

if not game_over(playing_board) and not len(blank_cells(playing_board)):
    print("\n\nThis game is tie")
else:
    wins(playing_board, opposit_symbol[MM], True)
    
print('Total Execution time:',sum(sum_total), 'ms')
