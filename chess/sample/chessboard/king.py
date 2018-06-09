import sample.helpers.constants
from .abstract_chess_piece import ChessPiece
from .abstract_chess_piece import out_of_bounds


class King(ChessPiece):
    def __init__(self, board, color, row, col):
        super().__init__(board, color, row, col, sample.helpers.constants.KING)

    def can_move(self, to_row, to_col):
        if abs(to_col - self.col) == 2 and to_row == self.row: # castle on either side
            if self.has_moved:
                return False
            if self.board.is_blocked(self.row, self.col, to_row, to_col): # TODO: Check if rook is blocked... prevents fringe case where an enemy piece is in the way of the check
                return False
            ## TODO: get rook, check if it's blocked. See if king would be in check with both moves that it would make
            ## TODO: if valid, switch em up

        if abs(to_col - self.col) <= 1 and abs(to_row - self.row) <= 1 and not self.is_current_position(to_row, to_col):
            curr_spot = self.board.get_square(to_row, to_col)
            return True if curr_spot is None or self.is_white() != curr_spot.is_white() else False
        return False

    def get_valid_moves(self):
        valid_moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                p_row, p_col = self.row + i, self.col + j
                if not (i == 0 and j == 0) and not out_of_bounds(p_row, p_col):
                    if self.try_move(p_row, p_col):
                        valid_moves.append((p_row, p_col))
        return valid_moves

