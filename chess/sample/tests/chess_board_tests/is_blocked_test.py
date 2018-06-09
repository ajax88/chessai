import unittest
from sample.helpers import constants
from sample.chessboard.chess_board import ChessBoard
from sample.chessboard.bishop import Bishop
from sample.chessboard.pawn import Pawn
from sample.chessboard.rook import Rook


class TestIsBlocked(unittest.TestCase):
    def test_initialization(self):
        ChessBoard()

    def test_flipped(self):
        ChessBoard(flip_board=True)

    def test_move(self):
        board = ChessBoard()
        p1 = board.get_pieces_of_color(constants.WHITE)[0]
        p1_row, p1_col = p1.get_position()

        self.assertEqual(p1.move(p1_row - 1, p1_col + 1), False)

    def test_is_blocked_horz(self):
        board = ChessBoard()
        rook = Rook(board, constants.WHITE, 5, 2)
        board.set_square(rook)

        # Test horiz. non-blocked
        # Rook 5,2 --> 5,6
        self.assertEqual(board.is_blocked(5, 2, 5, 6), False)
        # Rook 5,2 --> 5,0
        self.assertEqual(board.is_blocked(5, 2, 5, 0), False)

        self.assertEqual(board.is_blocked(5, 2, 6, 2), True)

    def test_is_blocked_vert(self):
        board = ChessBoard()

        rook = Rook(board, constants.WHITE, 5, 2)
        board.set_square(rook)

        #Test vert. non blocked
        self.assertEqual(board.is_blocked(5, 2, 2, 2), False)
        rook.set_position(2, 3)
        board.set_square(rook)
        self.assertEqual(board.is_blocked(2, 3, 5, 3), False)

    def test_is_blocked_diag(self):
        board = ChessBoard()

        #Test diagonal directions non blocked
        bishop = Bishop(board, constants.WHITE, 4, 4)
        board.set_square(bishop)
        self.assertEqual(board.is_blocked(4, 4, 2, 2), False)
        self.assertEqual(board.is_blocked(4, 4, 2, 6), False)
        self.assertEqual(board.is_blocked(4, 4, 5, 3), False)
        self.assertEqual(board.is_blocked(4, 4, 5, 5), False)

    def test_is_blocked_missing_start_piece(self):
        board = ChessBoard()
        #Test error cases:
        # No piece exists at start position
        with (self.assertRaises(ValueError)):
            board.is_blocked(3, 3, 4, 4)

    def test_is_blocked_invalid_path(self):
        board = ChessBoard()
        bishop = Bishop(board, constants.WHITE, 3, 1)
        board.set_square(bishop)
        # Non straight path given
        with (self.assertRaises(ValueError)):
            board.is_blocked(3, 1, 4, 4)

    def test_is_blocked_taking_piece(self):
        board = ChessBoard(debug=True)
        p1 = Pawn(board, constants.WHITE, 4, 3)
        p2 = Pawn(board, constants.BLACK, 3, 4)
        board.set_square(p1)
        board.set_square(p2)
        p3 = Pawn(board, constants.BLACK, 2, 1)
        board.set_square(p3)
        p4 = Pawn(board, constants.BLACK, 6, 1)
        board.set_square(p4)
        p5 = Pawn(board, constants.BLACK, 6, 5)
        board.set_square(p5)
        p6 = Pawn(board, constants.BLACK, 4, 5)
        board.set_square(p6)
        p7 = Pawn(board, constants.BLACK, 4, 0)
        board.set_square(p7)
        p8 = Pawn(board, constants.BLACK, 1, 3)
        board.set_square(p8)
        p9 = Pawn(board, constants.BLACK, 5, 3)
        board.set_square(p9)

        self.assertEqual(board.is_blocked(4, 3, 6, 5), False)
        self.assertEqual(board.is_blocked(4, 3, 2, 1), False)
        self.assertEqual(board.is_blocked(4, 3, 3, 4), False)
        self.assertEqual(board.is_blocked(4, 3, 6, 1), False)
        self.assertEqual(board.is_blocked(4, 3, 4, 5), False)
        self.assertEqual(board.is_blocked(4, 3, 4, 0), False)
        self.assertEqual(board.is_blocked(4, 3, 1, 3), False)
        self.assertEqual(board.is_blocked(4, 3, 5, 3), False)


if __name__ == '__main__':
    unittest.main()


