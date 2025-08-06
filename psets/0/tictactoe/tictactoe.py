"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Keep track of X and O in the board
    count_x = 0
    count_o = 0

    for row in board:
        for column in row:
            if column == X:
                count_x += 1
            elif column == O:
                count_o += 1

    # If count_o is equal to count_x or all the cells are empty (the count will be the same either way), X moves
    if count_o == count_x:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    # Keep track of possible moves
    possible_moves = set()

    # Calculate the quantity of rows and colums in the board
    board_rows = range(len(board)) 
    board_columns = range(len(board[0]))

    # Get all positions where there is no X or O
    for row in board_rows:
        for column in board_columns:
            if board[row][column] == EMPTY:
                possible_moves.add((row, column))

    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Initialize a new board based os the state of the board passed
    resulted_board = copy.deepcopy(board)

    # Get the next move location
    i, j = action

    # Verify if the move is out of bounds
    board_rows = len(board)
    board_columns = len(board[0])
    if i > board_rows or j > board_columns or i < 0 or j < 0:
        raise ValueError(f"Position ({i},{j}) invalid, out of bounds")

    if resulted_board[i][j] != EMPTY:
        raise ValueError("Action not possible, the position in not empty")

    # Make the next move
    resulted_board[i][j] = player(board)

    return resulted_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Horizontal
    if (board[0][0] != EMPTY and board[0][0] == board[0][1] and board[0][1] == board[0][2]):
        return board[0][0]
    elif (board[1][0] != EMPTY and board[1][0] == board[1][1] and board[1][1] == board[1][2]): 
        return board[1][0]
    elif (board[2][0] != EMPTY and board[2][0] == board[2][1] and board[2][1] == board[2][2]):
        return board[2][0]
    
    # Vertical
    if (board[0][0] != EMPTY and board[0][0] == board[1][0] and board[1][0] == board[2][0]):
        return board[0][0]
    elif (board[0][1] != EMPTY and board[0][1] == board[1][1] and board[1][1] == board[2][1]):
        return board[0][1]
    elif (board[0][2] != EMPTY and board[0][2] == board[1][2] and board[1][2] == board[2][2]):
        return board[0][2]
    
    # Diagonal
    if (board[0][0] != EMPTY and board[0][0] == board[1][1] and board[1][1] == board[2][2]):
        return board[0][0] 
    elif (board[0][2] != EMPTY and board[0][2] == board[1][1] and board[1][1] == board[2][0]):
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    game_winner = winner(board)
    is_tie = all([cell != EMPTY for row in board for cell in row]) and game_winner == None

    if game_winner != None or is_tie:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    player_winner = winner(board)

    if player_winner == X:
        return 1
    elif player_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Verify if the game has ended
    if terminal(board):
        return None
    
    current_player = player(board)
    best_move = None

    if current_player == X:
        best_value = float("-inf") # Initialize best_value as the lowest possible, because we want to maximaxe it

        for action in actions(board):
            value = min_value(result(board, action))

            if value > best_value:  # Select the highest value
                best_value = value
                best_move = action

    elif current_player == O:
        best_value = float("inf") # Initialize best_value as the highest possible, because we want to minimize it

        for action in actions(board):
            value = max_value(result(board, action))

            if value < best_value:  # Select the lowest value
                best_value = value
                best_move = action

    return best_move

# Helper fucntions
def max_value(board):
    """Return the maximun value possible to achieve on the current board."""

    if terminal(board):
        return utility(board)
    
    v = float("-inf")

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v

def min_value(board):
    """Return the minimun value possible to achieve on the current board."""

    if terminal(board):
        u = utility(board)
        return utility(board)
    
    v = float("inf")

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v