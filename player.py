import numpy as np
from board import Board

class Player:
    def __init__(self, ply, symbol):
        self.ply = ply
        self.symbol = symbol

    def heuristic(self, b):
        # find open spots
        return np.ones([len(b.state),len(b.state[0])])

    def minimax(self, b):
        return [0,0]


    def take_turn(self, b):
        if b.isEmpty():
            # assumes board is 2d 
            loc = [int(len(b.state[0])/2), int(len(b.state)/2)]
            self.move(b, loc)
        else:
            state = self.heuristic(b)
            best_move = self.minimax(state)
            self.move(b, best_move)

    # given set loc = [x, y] places symbol there if empty else error?
    def move(self, b, loc):
        if b.state[loc[1]][loc[0]] == '':
            b.state[loc[1]][loc[0]] = self.symbol
        else:
            raise ValueError('location already has value')