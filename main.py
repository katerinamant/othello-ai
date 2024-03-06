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
    gui.game(board, user_player, ai_player)

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
