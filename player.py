from board import Board
from move import Move


class Player:
    def __init__(self, max_depth: int, piece_val: int):
        self._max_depth = max_depth
        self._piece_val = piece_val

    def mini_max(self, board: Board, depth: int, alpha , beta , flag: int) -> tuple[int, Move]:
        if depth == self._max_depth or len(board.is_terminal()) == 0:
            return (board.evaluate(), board.last_move)

        children = board.get_children(flag)
        res = (float("-inf") if flag > 0 else float("inf"), None)
        for child in children:
            val = self.mini_max(child, depth + 1, alpha, beta, flag * -1)

            if flag > 0:
                if val[0] > res[0]:
                    res = (val[0], child.last_move)
                alpha = max(alpha, val[0])
            else:
                if val[0] < res[0]:
                    res = (val[0], child.last_move)
                beta = min(beta, val[0])

            if alpha >= beta:
                break  # Beta cutoff (pruning)
        return res

    @property
    def max_depth(self):
        return self._max_depth

    @max_depth.setter
    def max_depth(self, depth):
        self._max_depth = depth

    @property
    def piece_val(self):
        return self._piece_val

    @piece_val.setter
    def piece_val(self, val):
        self._piece_val = val
