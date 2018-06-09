from sample.chessboard.chess_board import ChessBoard
from sample.chessboard.knight import Knight
from sample.helpers import constants
from sample.game.chess_game import ChessGame
from sample.tests.chess_board_tests.game_test import GameTest


class TestValidMove(GameTest):
    def test_knight_move(self):
        my_board = ChessBoard()
        my_board.set_square(Knight(my_board, constants.WHITE, 3, 3))
        valid_knight_moves = {(1, 4), (1, 2), (2, 5), (2, 1), (4, 1), (4, 5), (5, 2), (5, 4)}
        self.assertEqual(valid_knight_moves, set(my_board.get_square(3, 3).get_valid_moves()))

    def test_knight_move_side(self):
        my_board = ChessBoard()
        my_board.set_square(Knight(my_board, constants.WHITE, 4, 0))
        valid_knight_moves = {(2, 1), (3, 2), (5, 2)}
        self.assertEqual(valid_knight_moves, set(my_board.get_square(4, 0).get_valid_moves()))

    def test_king_move(self):
        game = ChessGame(False, False)
        self.execute_expected_valid_move(game, "d4")
        self.execute_expected_valid_move(game, "e5")
        self.execute_expected_valid_move(game, "e5")
        self.execute_expected_valid_move(game, "d6")
        self.execute_expected_valid_move(game, "c3")
        self.execute_expected_valid_move(game, "e5")
        self.execute_expected_valid_move(game, "qd8")
        self.assertFalse(self.checkmate_checker(game, constants.BLACK))




