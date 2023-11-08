from board import Board

class Node:
    def __init__(self, board: Board):
        self._board: Board = board
        self._minimax_val: int = None
        self._children: list[Node] = None

    def get_children(self, piece_val: int):
        self._children = [
            Node(child)
            for child in self._board.get_children(piece_val)
        ]
        return self._children

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        self._board = board

    @property
    def minimax_val(self):
        return self._minimax_val

    @minimax_val.setter
    def minimax_val(self, val):
        self._minimax_val = val
