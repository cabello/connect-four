# -*- coding: utf-8 -*-

from types import ListType

CROSS = 'X'
ROUND = 'O'

DEFAULT_COLUMNS = 7
DEFAULT_ROWS = 6
MINIMUM_CONNECTED = 4

class ColumnFullException(Exception):
    pass

class Game:
    def __init__(self, columns=DEFAULT_COLUMNS, rows=DEFAULT_ROWS):
        self._columns = columns
        self._rows = rows
        self._pieces = []
        self._cross_pieces = []
        self._round_pieces = []

    def _drop_piece(self, piece, column):
        position = None

        # from rows to zero
        for y in reversed(range(self._rows)):
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

    def _vertical_win(self, piece):
        return self._check_win(piece, vertical=True)

    def _horizontal_win(self, piece):
        return self._check_win(piece, horizontal=True)

    def _check_win(self, piece, vertical=False, horizontal=False):
        if vertical:
            a,b = 0,1 # Column is index zero, row is index one
        elif horizontal:
            a,b = 1,0

        pieces = self._get_pieces(piece)

        if not self._minimum_pieces(pieces):
            return False

        victory = False

        # Only the columns/rows where there pieces need to be visited
        columns_or_rows = set(map(lambda i: i[a], pieces))
        for z in columns_or_rows:
            # Get the pieces at the column/row z
            col_or_row_pieces = filter(lambda i: i[a] == z, pieces)

            if not self._minimum_pieces(col_or_row_pieces):
                continue

            # Just look in the range of columns/rows where there are pieces
            w_start = min(col_or_row_pieces)[b]
            w_end = max(col_or_row_pieces)[b] + 1
            for w in range(w_start, w_end):
                connected = filter(lambda i:
                                   w <= i[b] <= w + (MINIMUM_CONNECTED - 1),
                                   col_or_row_pieces)
                if self._minimum_pieces(connected):
                    return True

        return victory

    def _diagonal_win(self, piece):
        pieces = self._get_pieces(piece)

        if not self._minimum_pieces(pieces):
            return False

        victory = False

        for x in range(self._columns - (MINIMUM_CONNECTED - 1)):
            # Check from bottom left to top right
            for y in reversed(range((MINIMUM_CONNECTED - 1), self._rows)):
                aux = []
                for z in range(MINIMUM_CONNECTED):
                    if (x+z, y-z) in pieces:
                        aux.append((x+z, y-z))
                if self._minimum_pieces(aux):
                    return True

            # Check from top left to bottom right
            for y in range(self._rows - (MINIMUM_CONNECTED - 1)):
                aux = []
                for z in range(MINIMUM_CONNECTED):
                    if (x+z, y+z) in pieces:
                        aux.append((x+z, y+z))
                if self._minimum_pieces(aux):
                    return True

        return victory

    def _minimum_pieces(self, pieces):
        return len(pieces) >= MINIMUM_CONNECTED

    def _get_pieces(self, piece):
        if piece == CROSS:
            pieces = self._cross_pieces
        elif piece == ROUND:
            pieces = self._round_pieces
        return pieces
