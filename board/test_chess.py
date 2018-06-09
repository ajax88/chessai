import unittest
from board.chessboard import ChessBoard


class TestTTT(unittest.TestCase):
    def test_init(self):
        chess_board = ChessBoard()

        state = chess_board.get_initial_state()
        chess_board.print(state)

    def test_copy(self):
        chess_board = ChessBoard()
        _, board, player, can_castle, legal_moves = chess_board.get_initial_state()

        new_board = chess_board.copy_board(board)
        new_board[5][5] = 'X'

        self.assertEqual(new_board[5][5], 'X')
        self.assertEqual(board[5][5], ' ')

    def test_square_iteration(self):
        chess_board = ChessBoard(debug=True)
        for s in chess_board.generate_inbetween_squares(6, 4, 0, 4):
            print(s)
        print('\n')
        for s in chess_board.generate_inbetween_squares(7, 7, 0, 0):
            print(s)
        print('\n')
        for s in chess_board.generate_inbetween_squares(7, 0, 0, 7):
            print(s)
        print('\n')
        for s in chess_board.generate_inbetween_squares(0, 0, 7, 7):
            print(s)
        print('\n')
        for s in chess_board.generate_inbetween_squares(0, 7, 7, 0):
            print(s)
        print('\n')

    def test_is_blocked(self):
        def print_block(s_row, s_col, e_row, e_col):
            print("Is blocked from ({}, {}) -> ({}, {})".format(s_row, s_col, e_row, e_col))
        print("Testing is blocked...")
        chess_board = ChessBoard(debug=True)
        state = chess_board.get_initial_state()
        prev_board, board, player, can_castle, _ = state
        red_state = (prev_board, board, player, can_castle)

        chess_board.print(state)

        row_col = (6, 4, 1, 4)
        print_block(*row_col)
        self.assertFalse(chess_board.is_blocked(red_state, *row_col))

        row_col = (6, 4, 0, 4)
        print_block(*row_col)
        self.assertTrue(chess_board.is_blocked(red_state, *row_col))








