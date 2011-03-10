# -*- coding: utf-8 -*-

import unittest

from lib.game import Game, ColumnFullException

class GameTestCase(unittest.TestCase):
    def test_new_game(self):
        g = Game()
        self.assertTrue(isinstance(g, Game))

    def test_new_game_accepts_board_size(self):
        g = Game(rows=6, columns=7)
        self.assertTrue(isinstance(g, Game))
        self.assertEquals(g._rows, 6)
        self.assertEquals(g._columns, 7)

    def test_drop_piece_returns_final_position(self):
        g = Game() # 6x7 by default
        self.assertEquals(g._drop_piece('X', 0), (0,5))
        self.assertEquals(g._drop_piece('X', 0), (0,4))
        self.assertEquals(g._drop_piece('X', 0), (0,3))
        self.assertEquals(g._drop_piece('O', 0), (0,2))
        self.assertEquals(g._drop_piece('X', 0), (0,1))
        self.assertEquals(g._drop_piece('X', 0), (0,0))

    def test_drop_piece_on_full_column_raises(self):
        g = Game(rows=2)
        self.assertEquals(g._drop_piece('X', 0), (0,1))
        self.assertEquals(g._drop_piece('X', 0), (0,0))
        self.assertRaises(ColumnFullException, g._drop_piece, 'X', 0)

    def test_drop_cross(self):
        g = Game()
        self.assertEquals(g.drop_cross(0), (0,5))
        self.assertTrue((0,5) in g._cross_pieces)

    def test_drop_cross_on_full_column_raises(self):
        g = Game(rows=2)
        self.assertEquals(g.drop_cross(0), (0,1))
        self.assertEquals(g.drop_cross(0), (0,0))
        self.assertRaises(ColumnFullException, g.drop_cross, 0)

    def test_drop_round(self):
        g = Game()
        self.assertEquals(g.drop_round(0), (0,5))
        self.assertTrue((0,5) in g._round_pieces)

    def test_drop_round_on_full_column_raises(self):
        g = Game(rows=2)
        self.assertEquals(g.drop_round(0), (0,1))
        self.assertEquals(g.drop_round(0), (0,0))
        self.assertRaises(ColumnFullException, g.drop_round, 0)

if __name__ == "__main__":
    unittest.main()
