import numpy as np

class Board:
    def __init__(self):
        self.state = np.empty([6,6], dtype=str)
        self.empty = np.empty([6,6], dtype=str)
        self.winner = ''

    def isEmpty(self):
        return np.array_equal(self.state, self.empty)

    def wins(self, symbol):
        board = self.state
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if j < board.shape[1] - 3 and board[i][j] and symbol == board[i][j] == board[i][j + 1] == board[i][j + 2] == \
                        board[i][j + 3]:
                    self.winner = symbol
                if i < board.shape[0] - 3 and board[i][j] and symbol == board[i][j] == board[i + 1][j] == board[i + 2][j] == \
                        board[i + 3][j]:
                    self.winner = symbol
                if i < board.shape[0] - 3 and j < board.shape[1] - 3 and symbol == board[i][j] and board[i][j] == \
                        board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3]:
                    self.winner = symbol
                if i < board.shape[0] - 3 and j > 3 and board[i][j] and symbol == board[i][j] == board[i + 1][j - 1] == \
                        board[i + 2][j - 2] == board[i + 3][j - 3]:
                    self.winner = symbol
