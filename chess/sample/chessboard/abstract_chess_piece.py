# Base class for all other chess pieces
from abc import ABCMeta, abstractmethod

import sample.chessboard.chess_board
import sample.helpers.constants


class ChessPiece():
    metaclass = ABCMeta

    def __init__(self, board, color, row, col, name):
        if type(board) != sample.chessboard.chess_board.ChessBoard:
            raise TypeError("Must input valid chessboard.")

        if (color.lower() != sample.helpers.constants.WHITE) and (color.lower() != sample.helpers.constants.BLACK):
            raise ValueError("Color must be black or white.")

        self.name = name
        self.board = board
        self.color = color.lower()
        self.set_position(row, col)
        self.has_moved = False

    def get_name(self):
        return self.name

    def set_position(self, row, col):
        if out_of_bounds(row, col):
            raise ValueError('Index out of bounds')
        self.row = row
        self.col = col

    def get_position(self):
        return self.row, self.col

    def is_white(self):
        return self.color == sample.helpers.constants.WHITE

    def is_black(self):
        return not self.is_white()

    def set_board(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def set_has_moved(self, has_moved):
        self.has_moved = has_moved

    def has_moved(self):
        return self.has_moved

    def is_current_position(self, to_row, to_col):
        return self.row == to_row and self.col == to_col

    def change_board(self, to_row, to_col):
        self.board.set_square(sample.helpers.constants.BLANK, self.row, self.col)
        piece = self.board.get_square(to_row, to_col)
        if piece is not None:
            self.board.get_pieces_of_color(piece.color).remove(piece)

        self.set_position(to_row, to_col)
        self.board.set_square(self)

    def move(self, to_row, to_col):
        if self.can_move(to_row, to_col):
            rollback = self.prep_rollback(to_row, to_col)
            self.change_board(to_row, to_col)
            in_check, _ = self.board.in_check(self.color)
            if in_check:
                rollback()
                raise ValueError(sample.helpers.constants.MOVE_KING_IN_CHECK)
            self.has_moved = True
            return True
        return False

    # similar to move, but will not actually move the piece. Just will return true if a piece can move to a square,
    # while accounting for check
    def try_move(self, to_row, to_col):
        if self.can_move(to_row, to_col):
            rollback = self.prep_rollback(to_row, to_col)
            self.change_board(to_row, to_col)
            in_check, _ = self.board.in_check(self.color)
            rollback()
            return not in_check
        return False

    @abstractmethod
    def can_move(self, to_row, to_col):
        pass

    def prep_rollback(self, to_row, to_col):
        old_row, old_col = self.row, self.col
        old_piece = self.board.get_square(to_row, to_col)
        if old_piece is not None:
            old_piece_copy = old_piece.deep_copy()
            old_piece_copy.set_has_moved(old_piece.has_moved)

        def rollback():
            self.board.set_square(sample.helpers.constants.BLANK, self.row, self.col)
            self.row = old_row
            self.col = old_col
            self.board.set_square(self)
            if old_piece is not None:
                self.board.add_piece(old_piece_copy)

        return rollback

    def deep_copy(self):
        return type(self)(self.board, self.color, self.row, self.col)

    def __str__(self):
        return "{} {}: {}, {}".format(self.color, self.name, self.row, self.col)

    def __eq__(self, other):
        if other is not None and self.name == other.name and self.row == other.row and self.col == other.col and \
                        self.color == other.color:
            return True
        else:
            return False

    @abstractmethod
    def get_valid_moves(self):
        pass


def out_of_bounds(row, col):
    if row < 0 or row >= 8 or col < 0 or col >= 8:
        return True
    return False
