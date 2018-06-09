from sample.chessboard.chess_board import ChessBoard
from sample.chessboard.pawn import Pawn
from sample.helpers import constants
from sample.game.chess_game import ChessGame
from sample.tests.chess_board_tests.game_test import GameTest


class TestMove(GameTest):
    def test_basic_opening(self):
        game = ChessGame(False, True)
        comp_board = ChessBoard()

        self.classic_opening(game, comp_board)
        self.assertEqual(game.board, comp_board)
        self.execute_expected_valid_move(game, "c3")
        self.assertNotEqual(game.board, comp_board)

    def test_move_into_check(self):
        game = ChessGame(False, True)
        comp_board = ChessBoard()

        self.classic_opening(game, comp_board)
        self.execute_expected_error_move(game, "b3")

    def test_multiple_moves_into_check(self):
        game = ChessGame(False, True)
        comp_board = ChessBoard()

        self.classic_opening(game, comp_board)
        # c3
        comp_board.set_square(None, 6, 2)
        comp_board.set_square(Pawn(comp_board, constants.WHITE, 5, 2))
        self.execute_expected_error_move(game, "b3")
        self.execute_expected_error_move(game, "f4")
        self.execute_expected_valid_move(game, "c3")
        self.assertEqual(game.board, comp_board)





