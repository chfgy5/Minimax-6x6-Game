import numpy as np
from board import Board

class Player:
    def __init__(self, ply, symbol):
        self.ply = ply
        self.symbol = symbol

    def heuristic(self, node):
        return 1
    
    def minimax(self, b):
        return [0,0]

    def generate_states(self, b):
        height = len(b.state)
        length = len(b.state[0])
        states = np.zeros([height,length])
        for i in range(height):
            for j in range(length):
                if b.state[i][j] == '':
                    copy = np.copy(b.state)
                    copy[i][j] = self.symbol
                    states[i][j] = self.heuristic(copy)
                else: 
                    # can't move here, sentinel value?
                    copy[i][j] = 0
        return states

    def take_turn(self, b):
        if b.isEmpty():
            # assumes board is 2d 
            loc = [int(len(b.state[0])/2), int(len(b.state)/2)]
            self.move(b, loc)
        else:
            states = self.generate_states(b)
            best_move = self.minimax(states)
            self.move(b, best_move)

    # given set loc = [x, y] places symbol there if empty else error?
    def move(self, b, loc):
        if b.state[loc[1]][loc[0]] == '':
            b.state[loc[1]][loc[0]] = self.symbol
        else:
            raise ValueError('location already has value')