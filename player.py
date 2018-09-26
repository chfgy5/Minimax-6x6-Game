import numpy as np
from board import Board

class Player:
    def __init__(self, ply, symbol):
        self.ply = ply
        self.symbol = symbol

    def heuristic(self, node):
        score = 0
        # Evaluate score for each of the 8 lines (6 rows, 6 columns, 10 diagonals)
        for y in range(len(node)):
            score += self.evaluate_line(node[y].tolist())
        for x in range(len(node[0])):
            score += self.evaluate_line(node.T[x].tolist())

        return score
    
    def evaluate_line(self, row):
        me_three_row_two_side = 0
        opp_three_row_two_side = 0
        me_three_row_one_side = 0
        opp_three_row_one_side = 0
        me_open_two = 0
        opp_open_two = 0
        if ['',self.symbol,self.symbol,self.symbol,''] in row:
            me_three_row_two_side += 1
        elif ['',self.symbol,self.symbol,self.symbol] in row or [self.symbol,self.symbol,self.symbol,''] in row:
            me_three_row_one_side += 1
        elif ['',self.symbol,self.symbol] in row or [self.symbol,self.symbol,''] in row:
            me_open_two += 1
        
        if ['','O','O','O',''] in row:
            opp_three_row_two_side += 1
        if ['O'] in row:
            print("hi")

        return score

    
    def minimax(self, b):
        return np.unravel_index(np.argmax(b), b.shape)

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