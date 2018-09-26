import numpy as np

class Board:
    def __init__(self):
        self.state = np.empty([6,6], dtype=str)
        self.empty = np.empty([6,6], dtype=str)
        self.winner = ''

    def isEmpty(self):
        return np.array_equal(self.state, self.empty)

    def winner(player):
        self.winner = player