from player import *

b =  Board()
player1 = Player(2, 'X')
player2 = Player(4, 'O')

print(b.state)
player1.take_turn(b)
print(b.state)
player2.take_turn(b)
print(b.state)