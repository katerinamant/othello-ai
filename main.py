from gui import GUI
from player import Player
from board import Board


def welcome_screen() -> tuple[int, str]:
    """
    Show welcome window

    """
    print("\tWelcome to Othello AI!")
    difficulty, color = gui.welcome_window()

    if difficulty == None or color == None:
        # User closed the window without providing input
        return (None, None)

    if difficulty == "Novice":
        minimax_depth = 1
    elif difficulty == "Medium":
        minimax_depth = 3
    else:
        minimax_depth = 5
    user_input = color[0]

    return (minimax_depth, user_input)


def main():
    minimax_depth, user_input = welcome_screen()

    if minimax_depth == None or user_input == None:
        # User closed the window without providing input
        return

    if user_input == "B":
        user_player = Player(0, Board.B)
        ai_player = Player(minimax_depth, Board.W)
    else:
        user_player = Player(0, Board.W)
        ai_player = Player(minimax_depth, Board.B)

    board = Board()
    board.print_board()

    available_moves = {Board.W, Board.B}
    while available_moves:
        if board.last_player == Board.W:
            player_name = "black"
            piece = Board.B
        else:
            player_name = "white"
            piece = Board.W

        if piece not in available_moves:
            print(f"Sorry, there are no available moves for {player_name}!")
            board.last_player *= -1
            continue

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
            alpha = float("-inf")
            beta = float("inf")
            move = ai_player.mini_max(board, 0, alpha, beta, piece)[1]
            # We know it is a valid move
            # but the is_valid_move() function
            # also calculates the pieces to flip
            pieces_to_flip = board.is_valid_move(move.row, move.col, piece)
            board.make_move(move.row, move.col, piece, pieces_to_flip)
            print(
                f"{player_name[0].upper() + player_name[1:]} placed a piece on {move.row + 1} x {move.col + 1}"
            )

        board.print_board()
        available_moves = board.is_terminal()

    print("No valid moves for either player. The game is over.")

    if board.white_pieces == board.black_pieces:
        win_msg = "It's a tie!"
    else:
        winner = "White" if board.white_pieces > board.black_pieces else "Black"
        win_msg = f"{winner} wins {board.black_pieces} - {board.white_pieces}!"
    print(win_msg)

if __name__ == "__main__":
    gui = GUI()
    main()
