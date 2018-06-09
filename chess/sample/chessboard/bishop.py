import sample.helpers.constants
from sample.chessboard.abstract_chess_piece import ChessPiece
from sample.chessboard.abstract_chess_piece import out_of_bounds


class Bishop(ChessPiece):
    def __init__(self, board, color, row, col):
        super().__init__(board, color, row, col, sample.helpers.constants.BISHOP)

    def can_move(self, to_row, to_col):
        if abs(to_row - self.row) == abs(to_col - self.col):
            if not self.board.is_blocked(self.row, self.col, to_row, to_col):
                return True
        return False

    def get_valid_moves(self):
        valid_moves = []
        for i in range(-8, 9):
            if i != 0:
                # diag 'positive' slope
                p_row, p_col = self.row + i, self.col - i
                if not out_of_bounds(p_row, p_col):
                    if self.try_move(p_row, p_col):
                        valid_moves.append((p_row, p_col))
                # diag 'negative' slope
                p_row, p_col = self.row + i, p_col + i
                if not out_of_bounds(p_row, p_col):
                    if self.try_move(p_row, p_col):
                        valid_moves.append((p_row, p_col))

        return valid_moves
