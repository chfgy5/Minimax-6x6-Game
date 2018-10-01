from player import *

b =  Board()
player1 = Player(2, 'X', 'O')
player2 = Player(4, 'O', 'X')

while(1):
    player1.take_turn(b)
    print(b.state)
    b.wins(player1.symbol)
    if(b.winner != ''):
        break
    player2.take_turn(b)
    print(b.state)
    b.wins(player2.symbol)
    if(b.winner != ''):
        break

print("The winner is " +  b.winner)