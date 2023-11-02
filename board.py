import copy
from move import Move

class Board:
	W = 1
	B = -1
	EMPTY = 0
	DIMENSION = 8

	def __init__(self):
		self._game_board = []
		for _ in range(self.DIMENSION):
			self._game_board.append([self.EMPTY] * self.DIMENSION)
		# Set up Othello game board
		self._game_board[3][3] = self._game_board[4][4] = self.W
		self._game_board[4][3] = self._game_board[3][4] = self.B
		self._last_player = self.W  # black always plays first
		self._last_move = None
		self._available_pieces = self.DIMENSION ** 2

	def print_board(self):
		# Print column numbers
		print('\n  ', end='')
		for j in range(self.DIMENSION):
			print(f'  {j + 1}   ', end='')
		print(f"\n  {6*self.DIMENSION*'-'}")

		# Print rows
		for i in range(self.DIMENSION):
			print(f'{i + 1}|', end='')
			for j in range(self.DIMENSION):
				piece = ' '
				if self._game_board[i][j] == self.W:
					piece = 'O'
				elif self._game_board[i][j] == self.B:
					piece = 'X'
				print(f'  {piece}  |', end='')
			if i != self.DIMENSION - 1:
				print('\n')
		print(f"\n  {6*self.DIMENSION*'-'}\n")

	def get_children(self, letter):
		return list()

	def evaluate(self):
		return 0

	def is_terminal(self):
		# Board is filled completely
		return self._available_pieces == 0

	def is_valid_move(self, row, col):
		return not (row < 0 or row >= self.DIMENSION or
    				col < 0 or col >= self.DIMENSION or
    				self._game_board[row][col] != self.EMPTY)

	def make_move(self, row, col, letter):
		self._game_board[row][col] = letter
		self._available_pieces -= 1
		self._last_move = Move(row, col, letter)
		self._last_player = letter

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
	def game_board(self):
		return self._game_board

	@game_board.setter
	def game_board(self, g):
		self.game_board = copy.deepcopy(g)
