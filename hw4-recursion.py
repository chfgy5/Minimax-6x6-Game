import numpy as np
from math import inf as infinity
import random
import time
from os import system

MM = 'o'
opposit_symbol = {'o': 'x', 'x': 'o'}
board = np.zeros([6, 6], dtype=str)


# board[2] = ['','o','x','','','']
# board[3] = ['','o','o','x','','']
# board[4] = ['o','x','x','o','','']
# board[5] = ['','x','','','','']

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
        heuristics = {'x_3_row_2_side': [5, 0], 'o_3_row_2_side': [-10, 0], 'x_3_row_1_side': [3, 0],
                      'o_3_row_1_side': [-6, 0], 'x_2_row': [1, 0], 'o_2_row': [-1, 0]}
    else:
        heuristics = {'o_3_row_2_side': [5, 0], 'x_3_row_2_side': [-10, 0], 'o_3_row_1_side': [3, 0],
                      'x_3_row_1_side': [-6, 0], 'o_2_row': [1, 0], 'x_2_row': [-1, 0]}

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

            if i < board.shape[0] - 2 and j < board.shape[1] - 2 and board[i][j] and board[i][j] == board[i + 1][
                j + 1] == board[i + 2][j + 2]:
                temp = [board[i][j], board[i + 1][j + 1], board[i + 2][j + 2]]
                if 0 <= i - 1 < board.shape[0] and 0 <= j - 1 < board.shape[1]: temp = [board[i - 1][j - 1]] + temp
                if 0 <= i + 3 < board.shape[0] and 0 <= j + 3 < board.shape[1]: temp = temp + [board[i + 3][j + 3]]
                blank_check(temp, board[i][j], 3, heuristics)

            elif i < board.shape[0] - 1 and j < board.shape[1] - 1 and board[i][j] and board[i][j] == board[i + 1][
                j + 1]:
                temp = [board[i][j], board[i + 1][j + 1]]
                if 0 <= i - 1 < board.shape[0] and 0 <= j - 1 < board.shape[1]: temp = [board[i - 1][j - 1]] + temp
                if 0 <= i + 2 < board.shape[0] and 0 <= j + 2 < board.shape[1]: temp = temp + [board[i + 2][j + 2]]
                blank_check(temp, board[i][j], 2, heuristics)

            if i < board.shape[0] - 2 and j > 2 and board[i][j] and board[i][j] == board[i + 1][j - 1] == board[i + 2][
                j - 2]:
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


def wins(state, symbol):
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if j < board.shape[1] - 3 and board[i][j] and symbol == board[i][j] == board[i][j + 1] == board[i][j + 2] == \
                    board[i][j + 3]:
                return True
            if i < board.shape[0] - 3 and board[i][j] and symbol == board[i][j] == board[i + 1][j] == board[i + 2][j] == \
                    board[i + 3][j]:
                return True
            if i < board.shape[0] - 3 and j < board.shape[1] - 3 and symbol == board[i][j] and board[i][j] == \
                    board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3]:
                return True
            if i < board.shape[0] - 3 and j > 3 and board[i][j] and symbol == board[i][j] == board[i + 1][j - 1] == \
                    board[i + 2][j - 2] == board[i + 3][j - 3]:
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


def moves(state, symbol, desired_depth=0):
    depth = len(blank_cells(state))
    if depth == 0 or game_over(state):
        return
    if desired_depth > 0: depth = desired_depth

    print('Computer turn [{}]'.format(symbol))
    move = minimax(state, depth, symbol)
    i, j = move[0], move[1]
    state[i][j] = symbol
    print_board(board)


board = np.zeros([6, 6], dtype=str)
board[2][2] = 'x'
print_board(board)
current_move = 'o'
for i in range(100):
    MM = current_move
    moves(board, current_move, 2)
    current_move = opposit_symbol[current_move]









