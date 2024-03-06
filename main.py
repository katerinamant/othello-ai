from gui import GUI
from gui import WindowClosedError
from player import Player
from board import Board


def welcome_screen() -> tuple[int, str]:
    """
    Show welcome window

    """
    print("\tWelcome to Othello AI!")
    try:
        difficulty, color = gui.welcome_window()
    except WindowClosedError:
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
    gui.create_board_window(board, ai_player)

    available_moves = {Board.W, Board.B}
    while available_moves:
        if board.last_player == Board.W:
            player_name = "black"
            piece = Board.B
        else:
            player_name = "white"
            piece = Board.W

        if piece not in available_moves:
            gui.show_popup(f"Sorry, there are no available moves for {player_name}!")
            board.last_player *= -1
            continue

        print(f"Time for {player_name} to make a move!")
        if piece == user_player.piece_val:
            try:
                gui.user_move(board, user_player)
            except WindowClosedError:
                return
        else:
            alpha = float("-inf")
            beta = float("inf")
            move = ai_player.mini_max(board, 0, alpha, beta, ai_player.piece_val)[1]
            # We know it is a valid move
            # but the is_valid_move() function
            # also calculates the pieces to flip
            pieces_to_flip = board.is_valid_move(
                move.row, move.col, ai_player.piece_val
            )
            board.make_move(move.row, move.col, ai_player.piece_val, pieces_to_flip)
            print(
                f"{player_name[0].upper() + player_name[1:]} placed a piece on {move.row + 1} x {move.col + 1}"
            )
            try:
                gui.ai_move(board, ai_player, move.row, move._col)
            except WindowClosedError:
                return

        available_moves = board.is_terminal()

    gui.show_popup("No valid moves for either player. The game is over.")

    if board.white_pieces == board.black_pieces:
        win_msg = "It's a tie!"
    else:
        winner = "White" if board.white_pieces > board.black_pieces else "Black"
        win_msg = f"{winner} wins {board.black_pieces} - {board.white_pieces}!"
    gui.show_win_msg(win_msg)


if __name__ == "__main__":
    gui = GUI()
    main()
