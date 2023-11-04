from player import Player
from board import Board

if __name__ == "__main__":
    playerW = Player(0, Board.W)
    playerB = Player(0, Board.B)
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

        board.print_board()
    print("No valid moves for either player. The game is over.")
   
    for row in range(board.DIMENSION):
        for col in range(board.DIMENSION):
            res = 0
            for row in board._game_board:
                for col in board._game_board:
                    res += col

    winner = 'White' if res > 0 else 'Black'
    win_msg = f'{winner} player wins!' if res else "It's a tie!"
    print(win_msg)
