from __future__ import annotations
from move import Move
import copy


class Board:
    W: int = 1
    B: int = -1
    EMPTY: int = 0
    DIMENSION: int = 8

    def __init__(self):
        self._game_board: list[list[int]] = []
        for _ in range(self.DIMENSION):
            self._game_board.append([self.EMPTY] * self.DIMENSION)
        self._last_player: int = self.W  # black always plays first
        self._last_move: Move = None
        self._available_pieces: int = self.DIMENSION**2

        # Set up Othello game board
        self._game_board[3][3] = self._game_board[4][4] = self.W
        self._game_board[4][3] = self._game_board[3][4] = self.B
        self._black_pieces: int = 2
        self._white_pieces: int = 2

    def print_board(self):
        # Print column numbers
        print("\n  ", end="")
        for j in range(self.DIMENSION):
            print(f"  {j + 1}   ", end="")
        print(f"\tBlack (X): {self._black_pieces}")
        print(f"  {6*self.DIMENSION*'-'}", end="")
        print(f"\tWhite (O): {self._white_pieces}")

        # Print rows
        for i in range(self.DIMENSION):
            print(f"{i + 1}|", end="")
            for j in range(self.DIMENSION):
                piece = " "
                if self._game_board[i][j] == self.W:
                    piece = "O"
                elif self._game_board[i][j] == self.B:
                    piece = "X"
                print(f"  {piece}  |", end="")
            if i != self.DIMENSION - 1:
                print("\n")
        print(f"\n  {6*self.DIMENSION*'-'}\n")

    def get_children(self, piece_value: int) -> list[Board]:
        children: list[Board] = []
        for row in range(self.DIMENSION):
            for col in range(self.DIMENSION):
                pieces_to_flip = self.is_valid_move(row, col, piece_value)
                if pieces_to_flip:
                    child = Board()
                    child.game_board = self.game_board
                    child.make_move(row, col, piece_value, pieces_to_flip)
                    children.append(child)
        return children

    def evaluate(self) -> int:
        """
        Calculate the final evaluation score.

        Corners are worth 550 points, the sides are worth 200 points,
        and the number of available moves and the number of pieces
        on the board are worth 50 points each.

        If the return value is positive white has the edge over black,
        while if the return value is negative black has the edge.

        """
        res: int = 0
        board_corners: set[tuple[int, int]] = {
            (0, 0),
            (0, self.DIMENSION - 1),
            (self.DIMENSION - 1, 0),
            (self.DIMENSION - 1, self.DIMENSION - 1),
        }

        for row in range(self.DIMENSION):
            for col in range(self.DIMENSION):
                res += 50 * self._game_board[row][col]
                if (row, col) in board_corners:
                    res += 500 * self._game_board[row][col]
                elif (
                    row == 0
                    or col == 0
                    or row == self.DIMENSION - 1
                    or col == self.DIMENSION - 1
                ):
                    res += 150 * self._game_board[row][col]

                if self.is_valid_move(row, col, self.W):
                    res += 50
                if self.is_valid_move(row, col, self.B):
                    res -= 50
        return res

    def is_terminal(self) -> set[int]:
        """
        If there are no available pieces or if
        both players have no valid moves,
        the set is empty and the board is terminal.

        If the board is not terminal, we can use the
        resulting set to see which player has a valid move.

        """
        available = set()
        if self._available_pieces != 0:
            for row in range(self.DIMENSION):
                for col in range(self.DIMENSION):
                    if self.W not in available and self.is_valid_move(row, col, self.W):
                        available.add(self.W)
                    if self.B not in available and self.is_valid_move(row, col, self.B):
                        available.add(self.B)
                    if len(available) == 2:
                        break

        return available

    def get_neighbors(self, row: int, col: int) -> list[int]:
        neighbors = [
            (row - 1, col),
            (row - 1, col + 1),
            (row, col + 1),
            (row + 1, col + 1),
            (row + 1, col),
            (row + 1, col - 1),
            (row, col - 1),
            (row - 1, col - 1),
        ]
        return [nei for nei in neighbors if -1 not in nei and self.DIMENSION not in nei]

    def is_valid_move(self, row: int, col: int, piece_value: int) -> set[tuple[int]]:
        """
        Checks if a given player's move is valid.

        A move is considered valid if it is inside of the board's bounds
        and it sandwiches one or more opposing pieces in a line.

        """
        if (
            row not in range(0, self.DIMENSION)
            or col not in range(0, self.DIMENSION)
            or self._game_board[row][col] != self.EMPTY
        ):
            return set()

        pieces_to_flip = set()
        neighbors = self.get_neighbors(row, col)
        for x, y in neighbors:
            # Check if this piece placement correctly forms a sandwich
            # to at least one direction.
            self.check_valid_line(piece_value, x, y, x - row, y - col, pieces_to_flip)
        return pieces_to_flip

    def check_valid_line(
        self,
        piece_value: int,
        row: int,
        col: int,
        incr_row: int,
        incr_col: int,
        flip: set[tuple[int]],
    ) -> bool:
        """
        Recursively checks along a horizontal/vertical/diagonal line
        to see if there is a valid "sandwich" made by the color passed via piece_value.

        If there is a valid sandwich, it also adds the coordinates of the cells
        that should be converted (flipped) to the flip set.

        """
        if (
            row not in range(0, self.DIMENSION)
            or col not in range(0, self.DIMENSION)
            or self._game_board[row][col] == self.EMPTY
        ):
            return False

        if self._game_board[row][col] == piece_value:
            return True

        if not self.check_valid_line(
            piece_value, row + incr_row, col + incr_col, incr_row, incr_col, flip
        ):
            return False

        flip.add((row, col))
        return True

    def make_move(
        self, row: int, col: int, piece_value: int, pieces_to_flip: set[tuple[int]]
    ):
        """
        Registers the valid move made by a player and
        calls to flip the sandwiched enemy discs.

        """
        self._game_board[row][col] = piece_value
        self._available_pieces -= 1
        if piece_value == self.B:
            self._black_pieces += 1
        else:
            self._white_pieces += 1
        for x, y in pieces_to_flip:
            self.flip_disc(x, y)
        self._last_move = Move(row, col, piece_value)
        self._last_player = piece_value

    def flip_disc(self, row: int, col: int):
        if self._game_board[row][col] == self.B:
            self._black_pieces -= 1
            self._white_pieces += 1
        else:
            self._white_pieces -= 1
            self._black_pieces += 1
        self._game_board[row][col] *= -1

    @property
    def last_move(self):
        return self._last_move

    @last_move.setter
    def last_move(self, l):
        self._last_move = l

    @property
    def last_player(self):
        return self._last_player

    @last_player.setter
    def last_player(self, p):
        self._last_player = p

    @property
    def dimension(self):
        return self.DIMENSION

    @dimension.setter
    def dimension(self, d):
        self.DIMENSION = d

    @property
    def black_pieces(self):
        return self._black_pieces

    @property
    def white_pieces(self):
        return self._white_pieces

    @property
    def game_board(self):
        return self._game_board

    @game_board.setter
    def game_board(self, g):
        self._game_board = copy.deepcopy(g)
