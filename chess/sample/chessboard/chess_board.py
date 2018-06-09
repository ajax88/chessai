from sample.chessboard.king import King
from sample.chessboard.knight import Knight
from sample.chessboard.pawn import Pawn
from sample.chessboard.queen import Queen
from termcolor import colored

import sample.chessboard.abstract_chess_piece
from sample.helpers import constants
from sample.board.board import Board
from sample.chessboard.bishop import Bishop
from sample.chessboard.rook import Rook


class ChessBoard(Board):
    def __init__(self, flip_board=False, debug=False):
        super().__init__(8, 8)
        self.flip_board = flip_board
        self.debug = debug
        colors = [constants.WHITE, constants.BLACK]
        self.white_pieces = []
        self.black_pieces = []
        for i in range(8):
            # set up pawns
            self.add_piece(Pawn(self, colors[0 + self.flip_board], 6, i))
            self.add_piece(Pawn(self, colors[1 - self.flip_board], 1, i))

            # set up rooks
            if i == 0 or i == 7:
                self.add_piece(Rook(self, colors[0 + self.flip_board], 7, i))
                self.add_piece(Rook(self, colors[1 - self.flip_board], 0, i))

            # set up knights
            if i == 1 or i == 6:
                self.add_piece(Knight(self, colors[0 + self.flip_board], 7, i))
                self.add_piece(Knight(self, colors[1 - self.flip_board], 0, i))

            # set up bishops 
            if i == 2 or i == 5:
                self.add_piece(Bishop(self, colors[0 + self.flip_board], 7, i))
                self.add_piece(Bishop(self, colors[1 - self.flip_board], 0, i))

            # set up queen
            if i == 3:
                self.add_piece(Queen(self, colors[0 + self.flip_board], 7, i + flip_board))
                self.add_piece(Queen(self, colors[1 - self.flip_board], 0, i + flip_board))

            # set up king
            if i == 4:
                self.add_piece(King(self, colors[0 + self.flip_board], 7, i - flip_board))
                self.add_piece(King(self, colors[1 - self.flip_board], 0, i - flip_board))

    def set_square(self, piece, row = None, col = None):
        if not isinstance(piece, sample.chessboard.abstract_chess_piece.ChessPiece):
            if piece is not None:
                raise ValueError("Chessboard squares must take a piece")

        if piece is not None:
            row, col = piece.get_position()
        super(ChessBoard, self).set_square(row, col, piece)

    def get_pieces_of_color(self, color):
        return self.white_pieces if color == constants.WHITE else self.black_pieces

    def is_flipped(self):
        return self.flip_board

    def make_move(self, piece_type, color, destination_row, destination_col):
        if color == constants.WHITE:
            pieces = self.white_pieces
        else:
            pieces = self.black_pieces

        for piece in pieces:
            if piece.get_name() == piece_type:
                # TODO Duplicate piece move to same place?
                success = piece.move(destination_row, destination_col)
                if success:
                    return True
        return False

    def __str__(self):
        my_str = ''

        for i in range(self.row):

            # dash border
            my_str += ' '
            for _ in range(self.row):
                my_str += ' -'

            # side numbers 
            my_str += '\n'
            if not self.debug:
                my_str += str(self.flip_board * (i + 1) + (1 - self.flip_board) * (8 - i))
            else:
                my_str += str(i)

            my_str += '|'

            if not self.debug:
                for j in range(self.col):
                    piece = self.get_square(i, j)
                    piece_color = 'grey'
                    if piece is None:
                        char_piece = sample.helpers.constants.BLANK_CHAR
                    else:
                        char_piece = piece.get_name()
                        if piece.is_white():
                            piece_color = 'red'

                    if ((i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0)) - self.flip_board:
                        my_str += colored(char_piece, piece_color)
                    else:
                        my_str += colored(char_piece, piece_color, 'on_white')

                    my_str += '|'
            else:
                for j in range(self.col):
                    piece = self.get_square(i, j)
                    if piece is None:
                        my_str += sample.helpers.constants.BLANK_CHAR
                    else:
                        my_str += piece.get_name()
                    my_str += '|'

            my_str += '\n'
        # last dash border
        my_str += ' '
        for _ in range(self.row):
            my_str += ' -'
        if not self.debug:
            if not self.flip_board:
                my_str += '\n  a b c d e f g h'
            else:
                my_str += '\n  h f g e d c b a'
        else:
            my_str += '\n  0 1 2 3 4 5 6 7'
        return my_str

    def is_blocked(self, start_row, start_col, end_row, end_col):
        piece_list = [row_col for row_col in generate_inbetween_squares(start_row, start_col, end_row, end_col)]

        start_piece_is_white = False
        for i in range(len(piece_list)):
            row, col = piece_list[i]
            piece = self.get_square(row, col)
            if i == 0:
                if piece is None:
                        raise ValueError("Starting position in is_blocked must have piece.")
                else:
                    start_piece_is_white = piece.is_white()
            elif i == len(piece_list) - 1:
                if piece is not None and piece.is_white() == start_piece_is_white:
                    return True
            else:
                if piece is not None:
                    return True
        return False

    def get_pieces(self, name, color):
        to_return = []
        if color == constants.WHITE:
            for piece in self.white_pieces:
                if piece.get_name() == name:
                    to_return.append(piece)
        elif color == constants.BLACK:
            for piece in self.black_pieces:
                if piece.get_name() == name:
                    to_return.append(piece)
        return to_return

    def in_check(self, color):
        if color != constants.WHITE and color != constants.BLACK:
            raise ValueError(constants.INVALID_INPUT_COLOR)

        pieces_threatening_check = []
        if color == constants.WHITE:
            white_king = self.get_pieces(constants.KING, constants.WHITE)[0]
            for piece in self.black_pieces:
                row, col = white_king.get_position()
                if piece.can_move(row, col):
                    pieces_threatening_check.append(piece)

        if color == constants.BLACK:
            black_king = self.get_pieces(constants.KING, constants.BLACK)[0]
            for piece in self.white_pieces:
                row, col = black_king.get_position()
                if piece.can_move(row, col):
                    pieces_threatening_check.append(piece)

        if len(pieces_threatening_check) == 0:
            return False, pieces_threatening_check
        else:
            return True, pieces_threatening_check

    def add_piece(self, piece):
        self.set_square(piece)
        self.white_pieces.append(piece) if piece.color == constants.WHITE else self.black_pieces.append(piece)

    def __eq__(self, other):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.get_square(i, j) != other.get_square(i, j):
                    return False
        return True

    def game_over(self, color):
        valid_moves = list(filter(lambda lst: len(lst) != 0,
                           map(lambda piece: piece.get_valid_moves(), self.get_pieces_of_color(color))))
        if len(valid_moves) == 0:
            in_check, _ = self.in_check(color)
            return True, constants.CHECKMATE_MESSAGE if self.in_check(color) else constants.STALEMATE_MESSAGE
        return False, ""


# generates all squares between (start_row, start_col) -> (end_row, end_col), inclusive
def generate_inbetween_squares(start_row, start_col, end_row, end_col):
        # Ensure that boundary squares are unique
        if start_row == end_row and start_col == end_col:
            raise ValueError("generator must take unique positions.")

        # Case 1: Diagonal move
        r_dir, c_dir = 0, 0
        if abs(end_row - start_row) == abs(end_col - start_col):
            abs_distance = abs(end_row - start_row)
            # Determine if column and row values should increase or decrease to get
            # diagonal direction
            r_dir = -1 if (start_row - end_row) > 0 else 1
            c_dir = -1 if (start_col - end_col) > 0 else 1

        # Case 2: Horizontal move
        elif start_row == end_row:
            abs_distance = abs(start_col - end_col)
            c_dir = -1 if (start_col - end_col) > 0 else 1

        # Case 3: Vertical move
        elif start_col == end_col:
            abs_distance = abs(start_row - end_row)
            r_dir = -1 if (start_row - end_row) > 0 else 1

        else:
            raise ValueError("Inbetween generator must take straight path.")

        next_row, next_col = start_row, start_col
        yield (next_row, next_col)
        for _ in range(abs_distance):
            next_row += r_dir
            next_col += c_dir
            yield (next_row, next_col)
