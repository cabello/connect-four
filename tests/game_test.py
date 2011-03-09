# -*- coding: utf-8 -*-

import unittest

from lib.game import Game

class GameTestCase(unittest.TestCase):
    def test_new_game(self):
        g = Game()
        self.assertTrue(isinstance(g, Game))

    def test_new_game_accepts_board_size(self):
        g = Game(rows=6, columns=7)
        self.assertTrue(isinstance(g, Game))
        self.assertEquals(g._rows, 6)
        self.assertEquals(g._columns, 7)

if __name__ == "__main__":
    unittest.main()
