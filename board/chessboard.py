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
    ####################################################################################################################
    ########################################## PUBLIC METHODS ##########################################################
    ####################################################################################################################
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
        reduced_state = (None, board, WHITE_PLAYER, True, True, True, True)
        # Prev board, current board, player, can castle, legal_moves
        legal_moves = self.generate_legal_moves(reduced_state)

        return reduced_state + (legal_moves,)

    def get_state(self, state, action):
        prev_board, curr_board, player, p1ck, p1cq, p2ck, p2cq, legal_moves = state

        # check if action is in moves
        # make action, do appropriate edge checks (e.g pawn promotion)
        if action not in legal_moves:
            raise ValueError("Invalid move {}".format(action))

        new_prev = self.copy_board(curr_board)
        new_board = self.copy_board(curr_board)
        r, c, e_r, e_c = action
        new_board[e_r][e_c] = new_board[r][c]
        new_board[r][c] = EMPTY_SQUARE
        # TODO update castling!!
        # TODO execute empassant (delete pawn above)

        new_player = self.get_other_player(player)
        reduced_state = (new_prev, new_board, new_player, p1ck, p1cq, p2ck, p2cq)
        legal_moves = self.generate_legal_moves(reduced_state)

        return reduced_state + (legal_moves,)

    def get_legal_moves(self, state):
        _, _, _, _, _, _, _, legal_moves = state
        return legal_moves

    def ending_state(self, state):
        _, curr_board, player, _, _, _, _, legal_moves = state
        if legal_moves:
            return 0
        if self.king_in_check(curr_board, player):
            return 1
        else:
            return -1

    ####################################################################################################################
    #################################### METHODS TO GET LEGAL MOVES ####################################################
    ####################################################################################################################
    def generate_legal_moves(self, reduced_state):
        prev_board, curr_board, player, p1ck, p1cq, p2ck, p2cq = reduced_state
        moves = []
        for i in range(8):
            for j in range(8):
                p = curr_board[i][j]
                if p == EMPTY_SQUARE or self.get_player_of_piece(curr_board, i, j) != player:
                    continue
                p = p[1]
                if p == PAWN:
                    moves += self.get_pawn_moves(curr_board, player, i, j, prev_board)
                elif p == KNIGHT:
                    moves += self.get_knight_moves(curr_board, player, i, j)
                elif p == BISHOP:
                    moves += self.get_bishop_moves(curr_board, player, i, j)
                elif p == ROOK:
                    moves += self.get_rook_moves(curr_board, player, i, j)
                elif p == QUEEN:
                    moves += self.get_queen_moves(curr_board, player, i, j)
                elif p == KING:
                    moves += self.get_king_moves(curr_board, player, i, j, p1ck, p1cq, p2ck, p2cq)

        return moves

    def get_pawn_moves(self, board, player, row, col, prev_board):
        pawn_moves = []
        is_white = player == WHITE_PLAYER
        can_double = row == 6 * is_white + 1 * (not is_white)

        # check diag
        for i in range(-1, 2, 2):
            r = row + 1 + (-2 * is_white)
            c = col + i
            if self.in_bounds(r, c) and not self.will_cause_check(board, player, (row, col, r, c)):
                    p = board[r][c]
                    if (p != EMPTY_SQUARE and self.get_player_of_piece(board, r, c) != player) \
                            or (self.is_empassant(prev_board, board, player, (row, col, r, c))):
                        ## need to check empassant here
                        pawn_moves.append((row, col, r, c))
        # check single
        r = row + 1 + (-2 * is_white)
        if self.in_bounds(r, col) and not self.will_cause_check(board, player, (row, col, r, col)):
            p = board[r][col]
            if p == EMPTY_SQUARE:
                pawn_moves.append((row, col, r, col))

        # check_double
        d_row = row + 2 + (-4 * is_white)
        if can_double and not self.will_cause_check(board, player, (row, col, d_row, col)) \
                and not self.is_blocked(board, player, (row, col, d_row, col)):
            p = board[d_row][col]
            if p == EMPTY_SQUARE:
                pawn_moves.append((row, col, d_row, col))

        return pawn_moves

    def is_empassant(self, prev_board, board, player, move):
        s_row, s_col, e_row, e_col = move
        is_white = player == WHITE_PLAYER
        if not s_row == 3 * is_white + 4 * (not is_white):
            return False

        target_pawn = (BLACK_DENOTER if is_white else WHITE_DENOTER) + PAWN
        prev_pawn = prev_board[e_row + 1 + (-2 * is_white)][e_col]
        if prev_pawn != target_pawn:
            return False

        new_prev_pawn = board[e_row + 1 + (-2 * is_white)][e_col]
        curr_pawn = board[e_row - 1 + (2 * is_white)][e_col]
        if curr_pawn != target_pawn and new_prev_pawn != EMPTY_SQUARE:
            return False
        return True

    def get_knight_moves(self, board, player, row, col):
        knight_moves = []
        for i in range(-2, 3, 4):
            for j in range(-1, 2, 2):
                e_row = row + i
                e_col = col + j
                if self.in_bounds(e_row, e_col) and not self.will_cause_check(board, player, (row, col, e_row, e_col)):
                    p = board[e_row][e_col]
                    if p == EMPTY_SQUARE or player != self.get_player_of_piece(board, e_row, e_col):
                        knight_moves.append((row, col, e_row, e_col))
                e_row = row + j
                e_col = col + i
                if self.in_bounds(e_row, e_col) and not self.will_cause_check(board, player, (row, col, e_row, e_col)):
                    p = board[e_row][e_col]
                    if p == EMPTY_SQUARE or player != self.get_player_of_piece(board, e_row, e_col):
                        knight_moves.append((row, col, e_row, e_col))

        return knight_moves

    def get_bishop_moves(self, board, player, row, col):
        bishop_moves = []
        for i in range(-8, 9):
            if i != 0:
                # diag 'positive' slope
                e_row, e_col = row + i, col - i
                if self.in_bounds(e_row, e_col):
                    if not self.is_blocked(board, player, (row, col, e_row, e_col)) \
                            and not self.will_cause_check(board, player, (row, col, e_row, col)):
                        bishop_moves.append((row, col, e_row, e_col))
                # diag 'negative' slope
                e_row, e_col = row + i, col + i
                if self.in_bounds(e_row, e_col):
                    if not self.is_blocked(board, player, (row, col, e_row, e_col)) \
                            and not self.will_cause_check(board, player, (row, col, e_row, col)):
                        bishop_moves.append((row, col, e_row, e_col))
        return bishop_moves

    def get_rook_moves(self, board, player, row, col):
        rook_moves = []
        for i in range(-8, 9):
            if i != 0:
                # horizontal
                e_row, e_col = row, col + i
                if self.in_bounds(e_row, e_col):
                    if not self.is_blocked(board, player, (row, col, e_row, e_col)) \
                            and not self.will_cause_check(board, player, (row, col, e_row, col)):
                        rook_moves.append((row, col, e_row, e_col))
                # vertical
                e_row, e_col = row + i, col
                if self.in_bounds(e_row, e_col):
                    if not self.is_blocked(board, player, (row, col, e_row, e_col)) \
                            and not self.will_cause_check(board, player, (row, col, e_row, col)):
                        rook_moves.append((row, col, e_row, e_col))
        return rook_moves

    def get_queen_moves(self, board, player, row, col):
        queen_moves = []
        for i in range(-8, 9):
            if i != 0:
                # diag 'positive' slope
                e_row, e_col = row + i, col - i
                if self.in_bounds(e_row, e_col):
                    if not self.is_blocked(board, player, (row, col, e_row, e_col)) \
                            and not self.will_cause_check(board, player, (row, col, e_row, col)):
                        queen_moves.append((row, col, e_row, e_col))
                # diag 'negative' slope
                e_row, e_col = row + i, col + i
                if self.in_bounds(e_row, e_col):
                    if not self.is_blocked(board, player, (row, col, e_row, e_col)) \
                            and not self.will_cause_check(board, player, (row, col, e_row, col)):
                        queen_moves.append((row, col, e_row, e_col))
                # horizontal
                e_row, e_col = row, col + i
                if self.in_bounds(e_row, e_col):
                    if not self.is_blocked(board, player, (row, col, e_row, e_col)) \
                            and not self.will_cause_check(board, player, (row, col, e_row, col)):
                        queen_moves.append((row, col, e_row, e_col))
                # vertical
                e_row, e_col = row + i, col
                if self.in_bounds(e_row, e_col):
                    if not self.is_blocked(board, player, (row, col, e_row, e_col)) \
                            and not self.will_cause_check(board, player, (row, col, e_row, col)):
                        queen_moves.append((row, col, e_row, e_col))
        return queen_moves

    def get_king_moves(self, board, player, row, col, p1ck, p1cq, p2ck, p2cq):
        ## TODO Castle
        king_moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                e_row, e_col = row + i, col + j
                if not (i == 0 and j == 0) and self.in_bounds(e_row, e_col):
                    if not self.is_blocked(board, player, (row, col, e_row, e_col)) \
                            and self.will_cause_check(board, player, (row, col, e_row, e_col)):
                        king_moves.append((row, col, e_row, e_col))
        return king_moves

    def copy_board(self, board):
        return [[board[i][j] for j in range(8)] for i in range(8)]

    ####################################################################################################################
    ########################################### KING CHECK LOGIC #######################################################
    ####################################################################################################################
    def king_in_check(self, board, player):
        pos = []
        king_pos = None
        for i in range(8):
            for j in range(8):
                p = board[i][j]
                if p == EMPTY_SQUARE:
                    continue
                p_player = self.get_player_of_piece(board, i, j)
                if p_player == player and p[1] == KING:
                    king_pos = (i, j)
                if p_player == self.get_other_player(player):
                    pos.append((i, j))

        for p in pos:
            try:
                if self.piece_can_move(board, self.get_other_player(player), (p + king_pos)):
                    return True
            except ValueError:
                continue
        return False

    def will_cause_check(self, board, player, move):
        s_row, s_col, e_row, e_col = move
        cb = self.copy_board(board)
        cb[e_row][e_col] = cb[s_row][s_col]
        cb[s_row][s_col] = EMPTY_SQUARE
        return self.king_in_check(cb, player)

    def piece_can_move(self, board, player, move):
        s_row, s_col, e_row, e_col = move
        p = board[s_row][s_col]
        if p == EMPTY_SQUARE or self.get_player_of_piece(board, s_row, s_col) != player:
            raise ValueError("Piece must exist on ({}, {})".format(s_row, s_col))
        p = p[1]
        if p == PAWN:
            return self.pawn_can_move(player, move)
        elif p == KNIGHT:
            return self.knight_can_move(move)
        elif p == BISHOP:
            return self.bishop_can_move(board, player, move)
        elif p == ROOK:
            return self.rook_can_move(board, player, move)
        elif p == QUEEN:
            return self.queen_can_move(board, player, move)
        elif p == KING:
            return self.king_can_move(move)
        else:
            raise ValueError("Invalid piece {}".format(p))

    def pawn_can_move(self, player, move):
        s_row, s_col, e_row, e_col = move
        is_white = player == WHITE_PLAYER
        target_moves = []
        for i in range(-1, 2, 2):
            r = s_row + 1 + (-2 * is_white)
            c = s_col + i
            if self.in_bounds(r, c):
                target_moves.append((s_row, s_col, r, c))
        if move in target_moves:
            return True
        return False

    def knight_can_move(self, move):
        s_row, s_col, e_row, e_col = move
        return (abs(s_col - e_col) == 2 and abs(s_row - e_row) == 1) or (abs(s_row - e_row) == 2 and abs(s_col - e_col) == 1)

    def bishop_can_move(self, board, player, move):
        s_row, s_col, e_row, e_col = move
        if abs(e_row - s_row) == abs(e_col - s_col):
            if not self.is_blocked(board, player, move):
                return True
        return False

    def rook_can_move(self, board, player, move):
        s_row, s_col, e_row, e_col = move
        if s_row == e_row or s_col == e_col:
            if not self.is_blocked(board, player, move):
                return True
        return False

    def queen_can_move(self, board, player, move):
        return not self.is_blocked(board, player, move)

    def king_can_move(self, move):
        s_row, s_col, e_row, e_col = move
        return abs(s_row - e_row) <= 1 and abs(s_col - e_col) <= 1
    ####################################################################################################################
    ############################################## AUX METHODS #########################################################
    ####################################################################################################################

    def is_blocked(self, board, player, move):
        s_row, s_col, e_row, e_col = move
        squares = [(row, col) for (row, col) in self.generate_inbetween_squares(s_row, s_col, e_row, e_col)]
        for i in range(len(squares)):
            r, c = squares[i]
            p = board[r][c]
            if i == len(squares) - 1:
                return p != EMPTY_SQUARE and not self.get_player_of_piece(board, r, c) == self.get_other_player(player)
            elif p != EMPTY_SQUARE:
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

    def get_other_player(self, player):
        return BLACK_PLAYER if player == WHITE_PLAYER else WHITE_PLAYER

    def in_bounds(self, row, col):
        return row < 8 and row >= 0 and col < 8 and col >=0

    def print(self, state):
        _, board, player, _, _, _, _, legal_moves = state
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
        else:
            print('  a  b  c  d  e  f  g  h')


