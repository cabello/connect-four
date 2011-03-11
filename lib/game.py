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

        if len(pieces) < 4:
            return False

        victory = False

        # Only the columns/rows where there pieces need to be visited
        columns_or_rows = set(map(lambda i: i[a], pieces))
        for z in columns_or_rows:
            # Get the pieces at the column/row z
            col_or_row_pieces = filter(lambda i: i[a] == z, pieces)

            if len(col_or_row_pieces) < 4:
                continue

            # Just look in the range of columns/rows where there are pieces
            w_start = min(col_or_row_pieces)[b]
            w_end = max(col_or_row_pieces)[b] + 1
            for w in range(w_start, w_end):
                connected = filter(lambda i: w <= i[b] <= w+3,
                                   col_or_row_pieces)
                if len(connected) == 4:
                    return True

        return victory

