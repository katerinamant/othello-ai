from player import Player
from board import Board
from node import Node

if __name__ == "__main__":
    playerW = Player(2, Board.W)
    playerB = Player(2, Board.B)
    board = Board()
    board.print_board()

    while not board.is_terminal():
        if board.last_player == Board.W:
            player_name = "black"
            piece = Board.B
        else:
            player_name = "white"
            piece = Board.W

        print(f"Time for {player_name} to make a move!")
        if piece == Board.W:
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
            move = playerB.mini_max(Node(board), 0, piece)[1]
            pieces_to_flip = board.is_valid_move(move.row, move.col, piece)
            board.make_move(move.row, move.col, piece, pieces_to_flip)

        board.print_board()
    print("No valid moves for either player. The game is over.")

    res = 0
    for row in board._game_board:
        for col in row:
            res += col

    winner = "White" if res > 0 else "Black"
    win_msg = f"{winner} player wins!" if res else "It's a tie!"
    print(win_msg)
