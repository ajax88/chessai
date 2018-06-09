import unittest
from sample.game.chess_game import ChessGame
from sample.helpers import constants
from sample.tests.chess_board_tests.game_test import GameTest


class TestCheckMate(GameTest):
    def test_fools_mate(self):
        game = ChessGame(False, True)
        game.player1.set_color(constants.WHITE)
        game.player2.set_color(constants.BLACK)
        
        self.execute_expected_valid_move(game, "e4")
        self.assertFalse(self.checkmate_checker(game, constants.BLACK))
        self.assertFalse(self.checkmate_checker(game, constants.WHITE))
        self.execute_expected_valid_move(game, "g5")
        self.assertFalse(self.checkmate_checker(game, constants.BLACK))
        self.assertFalse(self.checkmate_checker(game, constants.WHITE))
        self.execute_expected_valid_move(game, "d4")
        self.assertFalse(self.checkmate_checker(game, constants.BLACK))
        self.assertFalse(self.checkmate_checker(game, constants.WHITE))
        self.execute_expected_valid_move(game, "f6")
        self.assertFalse(self.checkmate_checker(game, constants.BLACK))
        self.assertFalse(self.checkmate_checker(game, constants.WHITE))
        self.execute_expected_valid_move(game, "qh5")
        self.assertTrue(self.checkmate_checker(game, constants.BLACK))
        self.assertFalse(self.checkmate_checker(game, constants.WHITE))

