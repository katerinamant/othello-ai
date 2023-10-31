import copy

from move import Move

class Board:
	W = 1
	B = -1
	EMPTY = 0

	def __init__(self):
		self._game_board = []
		for i in range(8):
			self._game_board.append([])
			for _ in range(8):
				self._game_board[i].append(self.EMPTY)
		self._last_player = self.W  # black always plays first
		self._last_move = None
		self._filled_cells = 0
		self._dimension = 0

	def print_board(self):
		# Print column numbers
		print('\n')
		for j in range(8):
			print('    ', j + 1, end='')
		print('\n  ', 48*'-')

		# Print rows
		for i in range(8):
			print(i + 1, '|', end='')
			for j in range(8):
				if self._game_board[i][j] == self.W:
					piece = 'W'
				elif self._game_board[i][j] == self.B:
					piece = 'B'
				else:
					piece = ' '
				print(' ', piece, ' |', end='')
			if i != 7: print('\n')
		print('\n  ', 48*'-', '\n')

	def get_children(self, letter):
		return list()

	def evaluate(self):
		return 0

	def is_terminal(self):
		# Board is filled completely
		return self._filled_cells == 8*8

	def is_valid_move(self, row, col):
		if (row < 0 or row > 7) or \
	  		(col < 0 or col > 7) or \
			(self._game_board[row][col] != self.EMPTY):
				return False
		return True

	def make_move(self, row, col, letter):
		self._game_board[row][col] = letter
		self._filled_cells += 1
		self._last_move = Move(row, col, letter)
		self._last_player = letter

	@property
	def last_move(self):
		return self._last_move

	@last_move.setter
	def last_move(self, l):
		self._last_move = l

	@last_move.setter
	def last_move(self, move_obj):
		self._last_move.row = move_obj.row
		self._last_move.col = move_obj.col
		self.last_move.value = move_obj.value

	@property
	def last_player(self):
		return self._last_player

	@last_player.setter
	def last_player(self, p):
		self._last_player = p

	@property
	def dimension(self):
		return self._dimension

	@dimension.setter
	def dimension(self, d):
		self._dimension = d

	@property
	def game_board(self):
		return self._game_board

	@game_board.setter
	def game_board(self, g):
		self.game_board = copy.deepcopy(g)
