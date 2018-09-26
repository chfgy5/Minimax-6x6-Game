# TODO:
* Get Heuristic function implemented
* Get Minimax function implemented

# Minimax-6x6-Game
Implement the minimax  algorithm to  play  a  two-player, four-in-a-row  game,  which  is a variation of tic-tac-toe: two players, X and O, take turns marking the spaces in a 6×6 grid. The player who succeeds in placing 4 of their marks consecutively in a horizontal, vertical, or diagonal row wins the game.

* h(n) = 5*[#of two-side-open-3-in-a-row for me]–10*[#of two-side-open-3-in-a-row for opponent]+ 3*[#of one-side-open-3-in-a-row for me]–6*[#of one-side-open-3-in-a-row for opponent]+[#of open-2-in-a-row for me] -[#of open-2-in-a-row for opponent]
    * “one-side-open-3-in-a-row”: there is a blank space at one end of a 3-in-a-row.
    * “two-side-open-3-in-a-row”: there are blank spaces at both ends of a 3-in-a-row.
    * “open-2-in-a-row”: there are blank spaces at one or both ends of a 2-in-a-row.