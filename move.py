class Move:
    def __init__(self, row, col, piece_value):
        self._row = row
        self._col = col
        self._piece_value = piece_value

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @property
    def piece_value(self):
        return self._piece_value

    @row.setter
    def row(self, row):
        self._row = row

    @col.setter
    def col(self, col):
        self._col = col

    @piece_value.setter
    def piece_value(self, piece_value):
        self._piece_value = piece_value
