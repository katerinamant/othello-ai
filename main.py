from player import Player
from board import Board
from node import Node

def welcome_screen() -> tuple[int, str]:
    """
    Print welcome messages and request necessary input

    """
    print("\tWelcome to Othello AI!")
    minimax_depth = None
    while True:
        try:
            while minimax_depth not in {1, 2, 3}:
                if minimax_depth: print("Invalid input!")
                print("Choose difficulty:")
                print("1 - Easy\n2 - Medium\n3 - Hard")
                minimax_depth = int((input(">> ")))
            break
        except ValueError:
            print("Invalid input!")

    print("")
    user_input = None
    while user_input != "B" and user_input != "W":
        if user_input: print("Invalid input!")
        print("Choose color! Remember, black goes first...\nBlack: B / White: W")
        user_input = input(">> ")

    return (minimax_depth, user_input)

if __name__ == "__main__":
    minimax_depth, user_input = welcome_screen()
    if user_input == "B":
        user_player = Player(0, Board.B)
        ai_player = Player(minimax_depth, Board.W)
    else:
        user_player = Player(0, Board.W)
        ai_player = Player(minimax_depth, Board.B)

    board = Board()
    board.print_board()

    available_moves = {Board.W, Board.B}
    while len(available_moves) != 0:
        if board.last_player == Board.W:
            player_name = "black"
            piece = Board.B
        else:
            player_name = "white"
            piece = Board.W

        if piece not in available_moves:
            print(f"Sorry, there are no available moves for {player_name}!")
            board.last_player *= -1
            break

        print(f"Time for {player_name} to make a move!")
        if piece == user_player.piece_val:
            while True:
                try:
                    x = int(input("Choose row: ")) - 1
                    y = int(input("Choose column: ")) - 1
                    pieces_to_flip = board.is_valid_move(x, y, piece)
                    if pieces_to_flip:
                        board.make_move(x, y, piece, pieces_to_flip)
                        break
                    else:
                        print("Invalid move! Try again...")
                except ValueError:
                    print("Invalid input! Try again...\n")
        else:
            print("Calculating...")
            move = ai_player.mini_max(Node(board), 0, piece)[1]
            # We know it is a valid move
            # but the is_valid_move() function
            # also calculates the pieces to flip
            pieces_to_flip = board.is_valid_move(move.row, move.col, piece)
            board.make_move(move.row, move.col, piece, pieces_to_flip)
            print(f"{player_name[0].upper() + player_name[1:]} placed a piece on {move.row + 1} x {move.col + 1}")

        board.print_board()
        available_moves = board.is_terminal()

    print("No valid moves for either player. The game is over.")

    res = 0
    for row in board._game_board:
        for col in row:
            res += col

    winner = "White" if res > 0 else "Black"
    win_msg = f"{winner} player wins!" if res else "It's a tie!"
    print(win_msg)
