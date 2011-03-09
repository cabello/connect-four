# -*- coding: utf-8 -*-

class ColumnFullException(Exception):
    pass

class Game:
    def __init__(self, rows=6, columns=7):
        self._rows = rows
        self._columns = columns
        self._pieces = []

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

