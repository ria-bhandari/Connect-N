"""
Play connect n game
1. Get all user input of number of rows, number of columns and number of pieces to win
2. Check if there is a vertical, horizontal or diagonal win
VERTICAL WIN: create a new game board using columns and then separate it so I can work with columns
HORIZONTAL WIN: separate/slice the board according to rows; check if the current player piece = new element on new board
DIAGONAL: 2 diagonals = left and right
    Main idea behind diagonals: the sum of the indices of the diagonal (use this to check each piece)
    Left diagonal: create a new list called diagonals and append each diagonal piece and then compare
    Right diagonal: reverse left diagonal then rotate and append the pieces plus compare
3. Check if there is a tie : if all pieces on board are not in any winning condition or blank

Setup game:
- Number of rows
- Number of columns
- Number of pieces to win
- Make board --> board depends on 'dimensions' + blank_character (this leads to displaying the board)
- Player 1 = 'X'
- Player 2 = 'O'

Play game:
- Start with player 1 selecting a column to play in
- Switch turns + keep showing what the players are playing
- Keep checking if there is a win so far based off of number_of_pieces_to_win
- End game if someone won otherwise continue

Announce results:
- Based on whether someone won or it is a tie
"""
from typing import TypedDict, TypeVar
T = TypeVar('T')


class GameState(TypedDict):
    """
    a class containing all important information for the game
    """
    game_board: list[list[str]]
    number_of_pieces_to_win: int
    pieces_to_play: list[str]
    current_player: int
    location_of_piece: list
    blank_space: str


def valid_int(any_variable, question: str) -> int:
    """
    general validation to check if the number entered is a valid integer
    :param any_variable: any variable entered by the user in this program
    :param question: in case input is not correct type, this 'question' is asked again
    :return: an integer
    """
    while not any_variable.isdigit():
        any_variable = input(question)
    any_variable = int(any_variable)
    return any_variable


def get_column_number() -> int:
    """
    gets the column number from the player
    :return: column number as integer
    """
    column = input("Enter the number of columns: ")
    column = valid_int(column, "Enter the number of columns: ")
    return column


def get_row_number() -> int:
    """
    gets the row number from the player
    :return: row number as an integer
    """
    row = input("Enter the number of rows: ")
    row = valid_int(row, "Enter the number of rows: ")
    return row


def make_game_board(number_of_rows: int, number_of_cols: int, blank_space: str) -> list:
    """
    makes the game board according to user input provided
    :param number_of_rows: integer of number of rows
    :param number_of_cols: integer of number of columns
    :param blank_space: "*"
    :return: list
    """
    game_board = []
    for row in range(number_of_rows):
        row = [blank_space] * (number_of_cols)
        game_board.append(row)
    return game_board


def display_board(game_board: list[list[str]], gamestate: GameState) -> None:
    """
    prints out the game board to show the players
    :param game_board: list of list of strings which is basically a 2D array
    :return: none
    """

    print(end = '  ')
    for header in range(len(game_board[0])):
        print(header, end = ' ')
    print()
    for row_index in range(len(gamestate['game_board'])):
        print(len(game_board) - row_index - 1, ' '.join(gamestate['game_board'][row_index]))


def setup_game() -> dict:
    """
    gets all the user input and stores it in a dictionary to be used throughout the program
    :return: a dictionary of all key values to use in the game
    """
    blank_space = '*'
    number_of_rows = get_row_number()
    number_of_columns = get_column_number()
    number_of_pieces_to_win = input("Enter the number of pieces in a row to win: ")
    number_of_pieces_to_win = valid_int(number_of_pieces_to_win, "Enter the number of pieces in a row to win: ")
    game_board = make_game_board(number_of_rows, number_of_columns, blank_space)
    pieces_to_play = ['X', 'O']
    location_of_piece = [0, 0]
    return {
        'game_board': game_board,
        'number_of_pieces_to_win': number_of_pieces_to_win,
        'pieces_to_play': pieces_to_play,
        'current_player': 1,
        'location_of_piece': location_of_piece,
        'blank_space': blank_space
    }


def get_row(row_index:int, game_state: GameState) -> int:
    """
    gets the row from the user
    :param row_index: the index of the row
    :param game_state: calls variables from the gamestate class
    :return: an integer
    """
    count = 0
    for col_index in range(len(game_state['game_board'][0])):
        if (game_state['game_board'][row_index][col_index]) == (game_state['pieces_to_play'][game_state['current_player'] - 1]):
            count += 1
        else:
            count = 0
        if count == game_state['number_of_pieces_to_win']:
            return count

    return count


def horizontal_win(game_state: GameState) -> bool:
    """
    checks if there is a horizontal win by using a count and a win variable
    :param game_state: calls the variables in the class gamestate
    :return: a boolean (win - True or False)
    """
    win = False
    for row in range(len(game_state['game_board'])):
        rows = get_row(row, game_state)
        if rows == game_state['number_of_pieces_to_win']:
            win = True
            return win


def get_column(col_index: int, game_state: GameState) -> list[str]:
    """
    gets the column to play in entered by the user
    :param col_index: index of column
    :param game_state: calls variables in gamestate class
    :return: a list of strings
    """
    count = 0
    for row in range(len(game_state['game_board'])):
        if (game_state['game_board'][row][col_index]) == (game_state['pieces_to_play'][game_state['current_player'] - 1]):
            count += 1
        else:
            count = 0
        if count == game_state['number_of_pieces_to_win']:
            return count
    return count


def vertical_win(game_state: GameState) -> bool:
    """
    checks if there is a vertical win in the game
    :param game_state: calls variables in gamestate class
    :return: a boolean (win - True or False)
    """
    win = False
    for col_index in range(len(game_state['game_board'][0])):
        column = get_column(col_index, game_state)
        if column == game_state['number_of_pieces_to_win']:
            win = True
            return win


def slice_down_right(game_state: GameState) -> int:
    """
    slices the right diagonal downwards
    :param game_state: calls variables in gamestate class
    :return: an integer
    """
    count = 0
    gameboard = game_state['game_board']
    curr_row = game_state['location_of_piece'][0]
    curr_column = game_state['location_of_piece'][1]
    current_piece = game_state['pieces_to_play'][game_state['current_player']-1]
    while curr_row >= 0:
        new_row = curr_row + 1
        new_col = curr_column - 1

        if new_col < 0 or new_row == len(gameboard):
            break
        else:
            if gameboard[curr_row][curr_column] == gameboard[new_row][new_col] and gameboard[curr_row][curr_column] == current_piece:
                count += 1
            else:
                count = 0
            if count == game_state['number_of_pieces_to_win']-1:
                return count
        curr_row = new_row
        curr_column = new_col
    return count


def slice_up_right(game_state: GameState) -> int:
    """
    slices the right diagonal upwards
    :param game_state: calls variables in gamestate class
    :return: an integer
    """
    count = 0
    gameboard = game_state['game_board']
    curr_row = game_state['location_of_piece'][0]
    curr_column = game_state['location_of_piece'][1]
    current_piece = game_state['pieces_to_play'][game_state['current_player'] - 1]
    while curr_row >= 0:
        new_row = curr_row - 1
        new_col = curr_column + 1
        if new_row < 0 or new_col== len(gameboard[0]):
            break
        else:
            if gameboard[curr_row][curr_column] == gameboard[new_row][new_col] and gameboard[curr_row][curr_column] == current_piece:
                count += 1
            else:
                count = 0
            if count == (game_state['number_of_pieces_to_win']-1):
                return count
        curr_row = new_row
        curr_column = new_col
    return count


def right_diagonal(game_state: GameState) -> int:
    """
    adds both the sliced sides of the right diagonal
    :param game_state: calls variables in gamestate class
    :return: an integer
    """
    lower_right = slice_down_right(game_state)
    upper_right = slice_up_right(game_state)
    return lower_right + upper_right


def slice_down_left(game_state: GameState) -> int:
    """
    slices the left diagonal downwards
    :param game_state: calls variables in gamestate class
    :return: an integer
    """
    count = 0
    gameboard = game_state['game_board']
    curr_row = game_state['location_of_piece'][0]
    curr_column = game_state['location_of_piece'][1]
    current_piece = game_state['pieces_to_play'][game_state['current_player'] - 1]
    while curr_row >= 0:
        new_row = curr_row - 1
        new_col = curr_column - 1
        if new_row < 0 or new_col <0:
            break
        else:
            if gameboard[curr_row][curr_column] == gameboard[new_row][new_col] and gameboard[curr_row][curr_column] == current_piece:
                count += 1
            else:
                count = 0
            if count == (game_state['number_of_pieces_to_win'] - 1):
                return count
        curr_row = new_row
        curr_column = new_col
    return count


def slice_up_left(game_state: GameState) -> int:
    """
    slices the left diagonal upwards
    :param game_state: calls variables in gamestate class
    :return: an integer
    """
    count = 0
    gameboard = game_state['game_board']
    curr_row = game_state['location_of_piece'][0]
    curr_column = game_state['location_of_piece'][1]
    current_piece = game_state['pieces_to_play'][game_state['current_player'] - 1]
    while curr_row < len(gameboard):
        new_row = curr_row + 1
        new_col = curr_column + 1
        if new_row >= len(gameboard) or new_col >= len(gameboard[0]) :
            break
        else:
            if gameboard[curr_row][curr_column] == gameboard[new_row][new_col] and gameboard[curr_row][curr_column]== current_piece:
                count += 1
            else:
                count = 0
            if count == (game_state['number_of_pieces_to_win'] - 1):
                return count
        curr_row = new_row
        curr_column = new_col
    return count


def left_diagonal(game_state: GameState) -> int:
    """
    adds both the sliced sides of the left diagonal
    :param game_state: calls variables in gamestate class
    :return: an integer
    """
    lower_left = slice_down_left(game_state)
    upper_left = slice_up_left(game_state)
    return lower_left + upper_left


def diagonal_win(game_state: GameState) -> bool:
    """
    checks if there is a diagonal win by comparing the totals gotten of each diagonal with the number of pieces to win
    :param game_state: calls variables in gamestate class
    :return: a boolean
    """
    left_d = left_diagonal(game_state)
    right_d = right_diagonal(game_state)
    return right_d >= (game_state['number_of_pieces_to_win']-1) or left_d >= (game_state['number_of_pieces_to_win']-1)


def someone_won(game_state:GameState) -> bool:
    """
    checks if someone won diagonally, vertically or horizontally
    :param game_state: calls variables in gamestate class
    :return: a boolean
    """
    return diagonal_win(game_state) or vertical_win(game_state) or horizontal_win(game_state)


def is_board_full(game_state: GameState) -> bool:
    """
    checks if the board is already full
    :param game_state: calls variables in gamestate class
    :return: a boolean
    """
    for row in game_state['game_board']:
        for piece in row:
            if piece == game_state['blank_space']:
                return False
    return True


def tie(game_state: GameState) -> bool:
    """
    checks if there is a tie in the game
    :param game_state: calls variables in gamestate class
    :return: a boolean
    """
    return is_board_full(game_state) and not someone_won(game_state)


def is_game_over(game_state: GameState) -> bool:
    """
    Check if the game is over
    :return: whether the game is over or not
    """
    return someone_won(game_state) or tie(game_state)


def switch_turn(game_state: GameState) -> GameState:
    """
    switches the player turn
    :param game_state: calls variables in gamestate class
    :return: the class gamestate
    """
    if game_state['current_player'] == 1:
        game_state['current_player'] = 2
    else:
        game_state['current_player'] = 1
    return game_state


def is_valid_move(player_move: str, game_state: GameState) -> bool:
    """
    checks if the move made by the player is valid
    :param player_move: a string - 'X' or 'O'
    :param game_state: calls variables in gamestate class
    :return: a boolean
    """
    if len(player_move) != 1:
        return False
    if not player_move.isdigit():
        return False
    player_move = int(player_move)
    if not (0 <= player_move < len(game_state['game_board'][0])):
        return False

    for row in game_state['game_board']:
        if row[player_move] == game_state['blank_space']:
            return True


def get_valid_move_from_player(game_state:GameState) -> int:
    """
    gets a valid move from the player
    :param game_state: calls variables in gamestate class
    :return: an integer of player move
    """
    current_player_turn = game_state['current_player']
    prompt = 'Enter the column you want to play in: '
    move = input(prompt)
    while not is_valid_move(move, game_state):
        move = input(prompt)
    move = int(move)
    return move


def announce_results(game_state: GameState) -> None:
    """
    announces the final results of the game
    :param game_state: calls variables in gamestate class
    :return: none
    """
    if someone_won(game_state):
        winner = game_state['current_player']
        print(f'Player {winner} won!')
    else:
        print('Tie Game')


def take_turn(game_state: GameState) -> GameState:
    """
    lets player take a turn
    :param game_state: calls variables in gamestate class
    :return: the class gamestate
    """
    column = get_valid_move_from_player(game_state)
    current_player_piece = game_state['pieces_to_play'][game_state['current_player'] - 1]
    for row in reversed(range(len(game_state['game_board']))):
        if game_state['game_board'][row][column] == game_state['blank_space']:
            game_state['game_board'][row][column] = current_player_piece
            game_state['location_of_piece'][0] = row
            game_state['location_of_piece'][1] = column
            break
    return game_state


def play_game(game_state: GameState) -> GameState:
    """
    plays the connect n game
    :param game_state: calls variables in gamestate class
    :return: the class gamestate
    """
    while not is_game_over(game_state):
        display_board(game_state['game_board'], game_state)
        game_state = take_turn(game_state)
        if someone_won(game_state):
            break
        game_state = switch_turn(game_state)
    display_board(game_state['game_board'], game_state)
    return game_state


def connectn() -> None:
    """
    calls all main functions to run this program and play the game
    :return: none
    """
    game_state = setup_game()
    play_game(game_state)
    announce_results(game_state)


connectn()