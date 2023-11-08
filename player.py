from node import Node


class Player:
    def __init__(self, max_depth: int, piece_val: int):
        self._max_depth = max_depth
        self._piece_val = piece_val

    def mini_max(self, node: Node, depth: int, flag: int):
        if depth == self._max_depth or node.board.is_terminal():
            return (node.board.evaluate(), node.board.last_move)

        children = node.get_children(flag)
        res = (float("-inf") if flag > 0 else float("inf"), None)
        for child in children:
            val = self.mini_max(child, depth + 1, flag * -1)
            if flag > 0 and val[0] > res[0] or flag < 0 and val[0] < res[0]:
                res = (val[0], child.board.last_move)
        return res

    @property
    def max_depth(self):
        return self._max_depth

    @max_depth.setter
    def max_depth(self, depth):
        self._max_depth = depth
