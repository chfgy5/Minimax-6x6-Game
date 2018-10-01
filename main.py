from player import *

b =  Board()
player1 = Player(2, 'X', 'O')
player2 = Player(2, 'O', 'X')

while(b.winner == ''):
    player1.take_turn(b)
    print(b.state)
    player2.take_turn(b)
    print(b.state)

print("The winner is {1}" % b.winner)