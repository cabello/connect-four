# -*- coding: utf-8 -*-

CROSS = 'X'
ROUND = 'O'

DEFAULT_ROWS = 6
DEFAULT_COLUMNS = 7
MINIMUM_CONNECTED = 4

class ColumnFullException(Exception):
    pass

class Game:
    def __init__(self, rows=DEFAULT_ROWS, columns=DEFAULT_COLUMNS):
        self._rows = rows
        self._columns = columns
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

        if piece == CROSS:
            pieces = self._cross_pieces
        elif piece == ROUND:
            pieces = self._round_pieces

        if len(pieces) < MINIMUM_CONNECTED:
            return False

        victory = False

        # Only the columns/rows where there pieces need to be visited
        columns_or_rows = set(map(lambda i: i[a], pieces))
        for z in columns_or_rows:
            # Get the pieces at the column/row z
            col_or_row_pieces = filter(lambda i: i[a] == z, pieces)

            if len(col_or_row_pieces) < MINIMUM_CONNECTED:
                continue

            # Just look in the range of columns/rows where there are pieces
            w_start = min(col_or_row_pieces)[b]
            w_end = max(col_or_row_pieces)[b] + 1
            for w in range(w_start, w_end):
                connected = filter(lambda i: w <= i[b] <= w+3,
                                   col_or_row_pieces)
                if len(connected) == MINIMUM_CONNECTED:
                    return True

        return victory

    def _diagonal_win(self, piece):
        if piece == CROSS:
            pieces = self._cross_pieces
        elif piece == ROUND:
            pieces = self._round_pieces

        if len(pieces) < MINIMUM_CONNECTED:
            return False

        victory = False

        for x in range(self._columns - 3):
            for y in reversed(range(3, self._rows)):
                count = 0
                for z in range(MINIMUM_CONNECTED):
                    if (x+z, y-z) in pieces:
                        count += 1
                if count == MINIMUM_CONNECTED:
                    return True

            for y in range(self._rows - 3):
                count = 0
                for z in range(MINIMUM_CONNECTED):
                    if (x+z, y+z) in pieces:
                        count += 1
                if count == MINIMUM_CONNECTED:
                    return True

        return victory

