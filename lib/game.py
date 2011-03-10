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
        if piece == CROSS:
            pieces = self._cross_pieces
        elif piece == ROUND:
            pieces = self._round_pieces

        if len(pieces) < 4:
            return False

        victory = False

        # Only the columns where there are pieces need to be visited
        columns = set(map(lambda i: i[0], pieces))
        for x in columns:
            # Get the pieces at the column x
            column_pieces = filter(lambda i: i[0] == x, pieces)

            if len(column_pieces) < 4:
                continue

            # Just look in the range of rows where there are pieces
            y_start = min(column_pieces)[1]
            y_end = max(column_pieces)[1] + 1
            for y in range(y_start, y_end):
                connected = filter(lambda i: y <= i[1] <= y+3,
                                   column_pieces)
                if len(connected) == 4:
                    return True

        return victory

