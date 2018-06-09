import sample.helpers.constants
from sample.chessboard.abstract_chess_piece import ChessPiece
from sample.chessboard.abstract_chess_piece import out_of_bounds


class Rook(ChessPiece):
    def __init__(self, board, color, row, col):
        super().__init__(board, color, row, col, sample.helpers.constants.ROOK)

    def can_move(self, to_row, to_col):
        if (to_col == self.col and not to_row == self.row) or (to_row == self.row and not to_col == self.col):
            if not self.board.is_blocked(self.row, self.col, to_row, to_col):
                return True
        return False

    def get_valid_moves(self):
        valid_moves = []
        for i in range(-8, 9):
            if i != 0:
                # horizontal
                p_col = self.col + i
                if not out_of_bounds(self.row, p_col):
                    if self.try_move(self.row, p_col):
                        valid_moves.append((self.row, p_col))
                # vertical
                p_row = self.row + i
                if not out_of_bounds(p_row, self.col):
                    if self.try_move(p_row, self.col):
                        valid_moves.append((p_row, self.col))
        return valid_moves
