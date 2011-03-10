# -*- coding: utf-8 -*-

CROSS = 'X'
ROUND = 'O'

class ColumnFullException(Exception):
    pass

class Game:
    def __init__(self, rows=6, columns=7):
        self._rows = rows
        self._columns = columns
        self._pieces = []
        self._cross_pieces = []
        self._round_pieces = []

    def _drop_piece(self, piece, column):
        position = None

        # from rows to zero
        for y in range(self._rows-1, -1, -1):
            if (column, y) not in self._pieces:
                position = (column, y)
                self._pieces.append(position)
                break

        if position is None:
            raise ColumnFullException()

        return position

    def drop_cross(self, column):
        position = self._drop_piece(CROSS, column)
        self._cross_pieces.append(position)
        return position

    def drop_round(self, column):
        position = self._drop_piece(ROUND, column)
        self._round_pieces.append(position)
        return position

