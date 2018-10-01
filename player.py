from board import *

class Player:
    def __init__(self, ply, symbol, opponent):
        self.ply = ply
        self.symbol = symbol
        self.opponent = opponent

    def heuristic(self, node):
        return self.evaluate_heuristic(node)

    def blank_check(self, string, symbol, length, hs):
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

    def evaluate_heuristic(self, board):
        heuristics = {'x_3_row_2_side': [5, 0], 'o_3_row_2_side': [-10, 0], 'x_3_row_1_side': [3, 0], 'o_3_row_1_side': [-6, 0], 'x_2_row': [1, 0], 'o_2_row': [-1, 0]}
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if j < board.shape[1] - 2 and board[i][j] and board[i][j] == board[i][j + 1] == board[i][j + 2]:
                    temp = [board[i][j], board[i][j + 1], board[i][j + 2]]
                    if 0 <= j - 1 < board.shape[1]: temp = [board[i][j - 1]] + temp
                    if 0 <= j + 3 < board.shape[1]: temp = temp + [board[i][j + 3]]
                    self.blank_check(temp, board[i][j], 3, heuristics)

                elif j < board.shape[1] - 1 and board[i][j] and board[i][j] == board[i][j + 1]:
                    temp = [board[i][j], board[i][j + 1]]
                    if 0 <= j - 1 < board.shape[1]: temp = [board[i][j - 1]] + temp
                    if 0 <= j + 2 < board.shape[1]: temp = temp + [board[i][j + 2]]
                    self.blank_check(temp, board[i][j], 2, heuristics)

                if i < board.shape[0] - 2 and board[i][j] and board[i][j] == board[i + 1][j] == board[i + 2][j]:
                    temp = [board[i][j], board[i + 1][j], board[i + 2][j]]
                    if 0 <= i - 1 < board.shape[0]: temp = [board[i - 1][j]] + temp
                    if 0 <= i + 3 < board.shape[0]: temp = temp + [board[i + 3][j]]
                    self.blank_check(temp, board[i][j], 3, heuristics)

                elif i < board.shape[0] - 1 and board[i][j] and board[i][j] == board[i + 1][j]:
                    temp = [board[i][j], board[i + 1][j]]
                    if 0 <= i - 1 < board.shape[0]: temp = [board[i - 1][j]] + temp
                    if 0 <= i + 2 < board.shape[0]: temp = temp + [board[i + 2][j]]
                    self.blank_check(temp, board[i][j], 2, heuristics)

                if i < board.shape[0] - 2 and j < board.shape[1] - 2 and board[i][j] and board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2]:
                    temp = [board[i][j], board[i + 1][j + 1], board[i + 2][j + 2]]
                    if 0 <= i - 1 < board.shape[0] and 0 <= j - 1 < board.shape[1]: temp = [board[i - 1][j - 1]] + temp
                    if 0 <= i + 3 < board.shape[0] and 0 <= j + 3 < board.shape[1]: temp = temp + [board[i + 3][j + 3]]
                    self.blank_check(temp, board[i][j], 3, heuristics)

                elif i < board.shape[0] - 1 and j < board.shape[1] - 1 and board[i][j] and board[i][j] == board[i + 1][j + 1]:
                    temp = [board[i][j], board[i + 1][j + 1]]
                    if 0 <= i - 1 < board.shape[0] and 0 <= j - 1 < board.shape[1]: temp = [board[i - 1][j - 1]] + temp
                    if 0 <= i + 2 < board.shape[0] and 0 <= j + 2 < board.shape[1]: temp = temp + [board[i + 2][j + 2]]
                    self.blank_check(temp, board[i][j], 2, heuristics)

                if i < board.shape[0] - 2 and j > 2 and board[i][j] and board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2]:
                    temp = [board[i][j], board[i + 1][j - 1], board[i + 2][j - 2]]
                    if 0 <= i - 1 < board.shape[0] and 0 <= j + 1 < board.shape[1]: temp = [board[i - 1][j + 1]] + temp
                    if 0 <= i + 3 < board.shape[0] and 0 <= j - 3 < board.shape[1]: temp = temp + [board[i + 3][j - 3]]
                    self.blank_check(temp, board[i][j], 3, heuristics)

                elif i < board.shape[0] - 1 and j > 1 and board[i][j] and board[i][j] == board[i + 1][j - 1]:
                    temp = [board[i][j], board[i + 1][j - 1]]
                    if 0 <= i - 1 < board.shape[0] and 0 <= j + 1 < board.shape[1]: temp = [board[i - 1][j + 1]] + temp
                    if 0 <= i + 2 < board.shape[0] and 0 <= j - 2 < board.shape[1]: temp = temp + [board[i + 2][j - 2]]
                    self.blank_check(temp, board[i][j], 2, heuristics)
        sum_h = sum([val[0] * val[1] for key, val in heuristics.items()])
        return sum_h


    def minimax(self, b, node_type, ply):
        if(ply == 0):
            return self.heuristic(b)

        h = 0
        for y in range(len(b)):
            for x in range(len(b[0])):
                if(b[y][x] == ''):
                    if node_type == "max":
                        b[y][x] = self.symbol
                        h = max(h, self.minimax(b, "min", ply - 1))
                        b[y][x] = ''
                    else:
                        b[y][x] = self.opponent
                        h = min(h, self.minimax(b, "max", ply - 1))
                        b[y][x] = ''
        return h

    def take_turn(self, b):
        if b.isEmpty():
            # assumes board is 2d 
            loc = [int(len(b.state[0])/2), int(len(b.state)/2)]
            self.move(b, loc)
        else:
            best_move = [-1, -1]
            best_val = -10000000
            for y in range(len(b.state)):
                for x in range(len(b.state[0])):
                    h = self.minimax(np.copy(b.state), 'max', self.ply)
                    if  h > best_val:
                        best_move = [x,y]
            self.move(b, best_move)

    # given set loc = [x, y] places symbol there if empty else error?
    def move(self, b, loc):
        if b.state[loc[1]][loc[0]] == '':
            b.state[loc[1]][loc[0]] = self.symbol
        else:
            raise ValueError('location already has value')
