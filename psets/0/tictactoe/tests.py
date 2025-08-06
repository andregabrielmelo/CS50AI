import tictactoe

X = "X"
O = "O"
E = None

board = [[X, E, O],
         [O, E, E],
         [X, X, E]]
print(tictactoe.player(board))
print(tictactoe.actions(board))