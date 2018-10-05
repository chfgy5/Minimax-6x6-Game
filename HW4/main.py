from player import *

b =  Board()
player1 = Player(2, 'X', 'O')
player2 = Player(4, 'O', 'X')

turn = 0
while(1):
    if(turn % 2 == 0):
        player1.take_turn(b)
    else:
        player2.take_turn(b)
    if(b.winner != ''):
        break
    turn += 1

print("The winner is " +  b.winner)