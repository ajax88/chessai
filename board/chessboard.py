from board.board import Board


EMPTY_SQUARE = ' '
WHITE_DENOTER = 'w'
BLACK_DENOTER = 'b'
PAWN = 'p'
KNIGHT = 'n'
BISHOP = 'b'
ROOK = 'r'
QUEEN = 'q'
KING = 'k'
WHITE_PLAYER = 1
BLACK_PLAYER = 2


class ChessBoard(Board):
    def __init__(self, **kwargs):
        super().__init__()
        self.debug = kwargs.get("debug", False)

    def get_initial_state(self):
        board = [[' ' for _ in range(8)] for _ in range(8)]
        for i in range(8):
            board[1][i] = BLACK_DENOTER + PAWN
            board[6][i] = WHITE_DENOTER + PAWN
            if i == 0 or i == 7:
                board[0][i] = BLACK_DENOTER + ROOK
                board[7][i] = WHITE_DENOTER + ROOK
            if i == 1 or i == 6:
                board[0][i] = BLACK_DENOTER + KNIGHT
                board[7][i] = WHITE_DENOTER + KNIGHT
            if i == 2 or i == 5:
                board[0][i] = BLACK_DENOTER + BISHOP
                board[7][i] = WHITE_DENOTER + BISHOP
            if i == 3:
                board[0][i] = BLACK_DENOTER + QUEEN
                board[7][i] = WHITE_DENOTER + QUEEN
            if i == 4:
                board[0][i] = BLACK_DENOTER + KING
                board[7][i] = WHITE_DENOTER + KING
        reduced_state = (None, board, WHITE_PLAYER, True)
        # Prev board, current board, player, can castle, legal_moves
        legal_moves = self.generate_legal_moves(reduced_state)

        return reduced_state + (legal_moves,)

    def get_state(self, state, action):
        prev_board, curr_board, player, can_castle, legal_moves = state

        # check if action is in moves

        # make action, do appropriate edge checks (e.g pawn promotion)



################################################################
        new_board = None
        new_can_castle = can_castle
################################################################
        new_prev = self.copy_board(curr_board)
        new_player = self.get_other_player(player)

        reduced_state = (new_prev, new_board, new_player, new_can_castle)
        legal_moves = self.generate_legal_moves(reduced_state)

        return reduced_state + (legal_moves,)

    def get_legal_moves(self, state):
        _, _, _, _, legal_moves = state
        return legal_moves

    def ending_state(self, state):
        raise NotImplementedError

    def get_other_player(self, player):
        return BLACK_PLAYER if player == WHITE_PLAYER else WHITE_PLAYER

    def can_move(self, reduced_state, s_row, s_col, e_row, e_col):
        _, board, player, _ = reduced_state
        if self.is_blocked(reduced_state, s_row, s_col, e_row, e_col):
            return False

        cb = self.copy_board(board)
        cb[e_row][e_col] = cb[s_row][s_col]
        cb[s_row][s_col] = EMPTY_SQUARE
        return self.king_in_check(cb, player)

    def is_blocked(self, board, player, s_row, s_col, e_row, e_col):
        squares = [(row, col) for (row, col) in self.generate_inbetween_squares(s_row, s_col, e_row, e_col)]
        for i in range(len(squares)):
            r, c = squares[i]
            p = board[r][c]
            if i == len(squares) - 1:
                return p != EMPTY_SQUARE and not self.get_player_of_piece(board, r, c) == self.get_other_player(player)
            elif p != EMPTY_SQUARE:
                return True
        return False

    def generate_legal_moves(self, reduced_state):
        prev_board, curr_board, player, can_castle = reduced_state
        return []

    def copy_board(self, board):
        return [[board[i][j] for j in range(8)] for i in range(8)]

    def king_in_check(self, board, player):
        pos = []
        king_pos = None
        for i in range(8):
            for j in range(8):
                p_player = self.get_player_of_piece(board, i, j)
                p = board[i][j]
                if p_player is player and p[1] is KING:
                    king_pos = (i, j)
                if p_player is self.get_other_player(player):
                    pos.append((i, j))

        for p in pos:
            if not self.is_blocked(board, self.get_other_player(player), *p, *king_pos):
                return True
        return False

    def get_player_of_piece(self, board, row, col):
        p = board[row][col]
        if p == EMPTY_SQUARE:
            raise ValueError("Square ({}, {}) must contain a piece".format(row, col))
        return WHITE_PLAYER if p[0] == WHITE_DENOTER else BLACK_PLAYER

    def generate_inbetween_squares(self, start_row, start_col, end_row, end_col):
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
        for _ in range(abs_distance):
            next_row += r_dir
            next_col += c_dir
            yield (next_row, next_col)

    def print(self, state):
        _, board, player, _, legal_moves = state
        print("Player {}'s turn.\n".format(player))
        if self.debug:
            print('  0  1  2  3  4  5  6  7')
        else:
            print('  a  b  c  d  e  f  g  h')
        c = 1
        for r in board:
            print('  ', end='')
            for i in range(8):
                if i == 7:
                    print('--')
                else:
                    print('--', end=' ')

            print(c - (self.debug * 1), end='|')
            i = 0
            for s in r:
                if i == 7:
                    print(s if len(s) == 2 else '  ', end='|\n')
                else:
                    print(s if len(s) == 2 else '  ', end='|')
                i += 1
            c += 1

        print('  ', end='')
        for i in range(8):
            if i == 7:
                print('--')
            else:
                print('--', end=' ')

        if self.debug:
            print('  0  1  2  3  4  5  6  7')
            print('The player\'s legal moves are {}'.format(legal_moves))
        else:
            print('  a  b  c  d  e  f  g  h')


