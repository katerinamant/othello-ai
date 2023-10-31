from player import Player
from board import Board

if __name__ == '__main__':
    playerW = Player(0, Board.W)
    playerB = Player(0, Board.B)
    board = Board()
    board.print_board()


