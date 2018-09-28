from board import *

class Player:
    def __init__(self, ply, symbol, opponent):
        self.ply = ply
        self.symbol = symbol
        self.opponent = opponent

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

        score = 5*me_three_row_two_side
        return score

    
    def minimax(self, b, node_type, ply):
        if(ply == 0):
            return self.heuristic(b)

        for y in range(len(b)):
            for x in range(len(b[0])):
                if(b[y][x] == ''):
                    if node_type == "max":
                        b[y][x] = self.symbol
                        h = self.minimax(b, "min", ply - 1)
                        b[y][x] = ''
                    else:
                        b[y][x] = self.opponent
                        h  = self.minimax(b, "max", ply - 1)
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