import sample.helpers.constants
from sample.chessboard.abstract_chess_piece import ChessPiece
from sample.chessboard.abstract_chess_piece import out_of_bounds


class Pawn(ChessPiece):
    def __init__(self, board, color, row, col):
        super().__init__(board, color, row, col, sample.helpers.constants.PAWN)
        self.going_up = True if (self.is_white() and not self.board.is_flipped()) or \
            (self.is_black() and self.board.is_flipped()) else False

    def can_move(self, to_row, to_col):
        # diagonal moves
        if to_col != self.col:
            if abs(to_col-self.col) != 1:
                return False
            else:
                if (to_row - self.row) == (-1 if self.going_up else 1):
                    to_square = self.board.get_square(to_row, to_col)
                    if to_square is None or to_square.is_white() == self.is_white():
                        return False
                    else:
                        return True
                else:
                    return False
        # two spaces forward
        elif (to_row - self.row) == 2 * (-1 if self.going_up else 1):
            if self.board.is_blocked(self.row, self.col, to_row, to_col) or self.has_moved:
                return False
            else:
                if self.board.get_square(to_row, to_col) is not None:
                    return False
                return True

        # once space forward
        elif (to_row - self.row) == (-1 if self.going_up else 1):
            if self.board.is_blocked(self.row, self.col, to_row, to_col):
                return False
            else:
                if self.board.get_square(to_row, to_col) is not None:
                    return False
                return True
        else:
            return False

    def get_valid_moves(self):
        valid_moves = []
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                p_row, p_col = self.row + i, self.col + j
                if not out_of_bounds(p_row, p_col):
                    if self.try_move(p_row, p_col):
                        valid_moves.append((p_row, p_col))
        for i in range(-2, 3):
            p_row = self.row + i
            if not i == 0 and not out_of_bounds(p_row, self.col):
                if self.try_move(p_row, self.col):
                    valid_moves.append((p_row, self.col))
        return valid_moves
