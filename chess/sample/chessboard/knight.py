import sample.helpers.constants
from sample.chessboard.abstract_chess_piece import ChessPiece
from sample.chessboard.abstract_chess_piece import out_of_bounds


class Knight(ChessPiece):
    def __init__(self, board, color, row, col):
        super().__init__(board, color, row, col, sample.helpers.constants.KNIGHT)

    def can_move(self, to_row, to_col):
        if (abs(to_row - self.row) == 1 and abs(to_col - self.col) == 2) or \
                (abs(to_col - self.col) == 1 and abs(to_row - self.row) == 2):
            poss_piece = self.board.get_square(to_row, to_col)
            if poss_piece is None or poss_piece.is_white() != self.is_white():
                return True
        return False

    def get_valid_moves(self):
        valid_moves = []
        # this could be better....
        for i in range(-1, 2, 2):
            two = 2 * i
            one = 1 * i
            row_two = self.row + two
            row_one = self.row + one

            col_two = self.col + two
            col_one = self.col + one
            col_one_minus = self.col - one
            col_two_minus = self.col - two
            self.try_append_move(row_one, col_two, valid_moves)
            self.try_append_move(row_one, col_two_minus, valid_moves)
            self.try_append_move(row_two, col_one, valid_moves)
            self.try_append_move(row_two, col_one_minus, valid_moves)

        return valid_moves

    def try_append_move(self, to_row, to_col, valid_moves):
        if not out_of_bounds(to_row, to_col):
            if self.try_move(to_row, to_col):
                valid_moves.append((to_row, to_col))
