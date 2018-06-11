import unittest
from board.chessboard import *
import random


chess_board = ChessBoard(debug=True)
class TestTTT(unittest.TestCase):
    def test_init(self):
        state = chess_board.get_initial_state()
        chess_board.print(state)

    def test_make_moves(self):
        state = chess_board.get_initial_state()
        chess_board.print(state)
        initial_moves = chess_board.get_legal_moves(state)

        print("Starting moves")
        print(initial_moves)

    def test_king_in_check(self):
        state = chess_board.get_initial_state()
        prev_board, board, player, p1ck, p1cq, p2ck, p2cq, _, legal_moves = state
        chess_board.print(state)
        player = force_move(board, player, (6, 3, 4, 3))
        self.assertFalse(chess_board.king_in_check(board, player))
        player = force_move(board, player, (1, 3, 3, 3))
        self.assertFalse(chess_board.king_in_check(board, player))
        player = force_move(board, player, (6, 2, 4, 2))
        self.assertFalse(chess_board.king_in_check(board, player))
        player = force_move(board, player, (1, 4, 2, 4))
        self.assertFalse(chess_board.king_in_check(board, player))
        player = force_move(board, player, (6, 4, 4, 4))
        self.assertFalse(chess_board.king_in_check(board, player))
        player = force_move(board, player, (0, 5, 4, 1))
        self.assertTrue(chess_board.king_in_check(board, player))
        chess_board.print((None, board, player, True, True, True, True, []))
        player = force_move(board, player, (7, 3, 6, 3))
        self.assertFalse(chess_board.king_in_check(board, player))
        chess_board.print((None, board, player, True, True, True, True, []))
        player = force_move(board, player, (0, 3, 3, 3))
        self.assertFalse(chess_board.king_in_check(board, player))

    def test_get_moves(self):
        state = chess_board.get_initial_state()
        prev_board, board, player, p1ck, p1cq, p2ck, p2cq, _, legal_moves = state
        board[3][3] = WHITE_DENOTER + BISHOP
        chess_board.print(state)
        print(chess_board.get_bishop_moves(board, player, 3, 3))

    def test_playout(self):
        print("Testing self_play")
        state = chess_board.get_initial_state()
        move_history = []
        try:
            while not chess_board.ending_state(state):
                print("\n\nGame state\n\n")
                chess_board.print(state)
                print("\n\nMove sequence: \n\n{}".format(move_history))
                legal_moves = chess_board.get_legal_moves(state)
                print("Make move:\n{}".format(legal_moves))
                move = input("Move?")
                move = list(move)
                move = tuple(list(filter(check_char, move)))
                move = tuple(map(int, move))
                while move not in legal_moves:
                    move = input("Move? that was wrong.")
                    move = tuple(list(filter(check_char, list(move))))
                    move = tuple(map(int, move))
                move_history.append(move)
                state = chess_board.get_state(state, move)
        except ValueError:
            print("Exception occurred. Move history:\n".format(move_history))

    def test_empassant(self):
        print("Test Empassant")
        state = chess_board.get_initial_state()
        move_seq = ((6, 4, 4, 4), (1, 4, 3, 4), (6, 3, 4, 3), (3, 4, 4, 3))
        state = recreate_state(state, move_seq)
        state = chess_board.get_state(state, (6, 2, 4, 2))
        chess_board.print(state)
        state = chess_board.get_state(state, (1, 0, 2, 0))
        chess_board.print(state)
        state = chess_board.get_state(state, (6, 0, 5, 0))
        chess_board.print(state)
        state = chess_board.get_state(state, (4, 3, 5, 2))
        chess_board.print(state)

    def test_prevent_checkmate(self):
        state = chess_board.get_initial_state()
        move_seq = [(7, 1, 5, 2), (0, 1, 2, 2), (5, 2, 3, 3), (2, 2, 4, 3)]
        state = recreate_state(state, move_seq)
        chess_board.print(state)

        state = chess_board.get_state(state, (3, 3, 1, 2))
        chess_board.print(state)
        print("Legal moves: \n{}".format(chess_board.get_legal_moves(state)))

    def test_katie_bug(self):
        state = chess_board.get_initial_state()
        move_seq = [(6, 3, 4, 3), (1, 2, 3, 2), (4, 3, 3, 2), (0, 6, 2, 5)]
        state = recreate_state(state, move_seq)
        chess_board.print(state)

        state = chess_board.get_state(state, (3, 2, 2, 2))
        chess_board.print(state)
        print("Legal moves: \n{}".format(chess_board.get_legal_moves(state)))

    def test_knight_bug(self):
        state = chess_board.get_initial_state()
        prev_board, board, player, p1ck, p1cq, p2ck, p2cq, _,  legal_moves = state
        board[7][4] = EMPTY_SQUARE
        board[4][3] = WHITE_DENOTER + KING
        state = chess_board.get_state(state, (6, 4, 5, 4))
        chess_board.print(state)
        state = chess_board.get_state(state, (0, 1, 2, 2))
        chess_board.print(state)
        print(chess_board.get_legal_moves(state))

    def test_null_tuple_concat(self):
        state = chess_board.get_initial_state()
        move_seq = [(6, 5, 4, 5), (0, 1, 2, 0), (6, 2, 5, 2), (0, 6, 2, 5), (6, 7, 5, 7), (2, 5, 0, 6), (6, 3, 4, 3), (1, 6, 2, 6), (7, 3, 5, 1), (1, 7, 2, 7), (7, 4, 6, 5), (0, 0, 0, 1), (6, 5, 5, 5), (1, 4, 2, 4), (6, 0, 4, 0), (0, 5, 3, 2), (7, 2, 5, 4), (3, 2, 2, 3), (5, 5, 6, 5), (0, 4, 0, 5), (6, 5, 5, 5), (1, 2, 2, 2), (5, 2, 4, 2), (2, 3, 1, 2), (5, 1, 5, 3), (1, 3, 2, 3), (5, 4, 7, 2), (1, 2, 3, 0), (5, 3, 6, 2), (3, 0, 6, 3), (7, 7, 6, 7), (0, 3, 1, 2), (7, 1, 6, 3), (2, 4, 3, 4), (6, 6, 5, 6), (0, 5, 1, 6), (4, 3, 3, 4), (1, 2, 2, 1), (6, 4, 4, 4), (1, 5, 2, 5), (6, 3, 7, 1), (2, 3, 3, 4), (6, 1, 4, 1), (2, 1, 4, 3), (6, 7, 6, 3), (0, 2, 2, 4), (7, 2, 6, 1), (2, 0, 3, 2), (6, 3, 6, 6), (1, 6, 1, 7), (6, 1, 5, 2), (0, 1, 0, 4), (5, 7, 4, 7), (4, 3, 2, 3), (7, 0, 6, 0), (2, 3, 1, 3), (6, 0, 6, 1), (1, 3, 1, 2), (6, 6, 6, 3), (0, 4, 0, 2), (6, 3, 6, 6), (1, 2, 3, 0), (6, 2, 7, 3), (0, 2, 0, 5), (7, 3, 3, 3), (3, 0, 4, 0), (3, 3, 1, 3), (2, 4, 1, 5), (6, 6, 6, 4), (3, 2, 1, 3), (6, 4, 5, 4), (1, 3, 3, 2), (4, 1, 3, 2), (0, 5, 0, 0), (7, 5, 6, 4), (1, 5, 3, 3), (5, 5, 4, 6), (4, 0, 3, 0), (6, 1, 2, 1), (3, 3, 4, 4), (5, 2, 3, 0), (4, 4, 3, 3), (4, 2, 3, 3), (0, 6, 1, 4), (4, 7, 3, 7), (0, 7, 0, 4), (3, 3, 2, 3), (1, 7, 1, 6), (5, 4, 5, 1), (1, 0, 2, 1), (5, 1, 3, 1), (0, 4, 0, 3), (2, 3, 1, 4), (2, 1, 3, 0), (4, 6, 5, 7), (3, 4, 4, 4), (6, 4, 7, 3), (0, 3, 7, 3), (5, 7, 6, 7), (7, 3, 6, 3), (6, 7, 5, 7), (6, 3, 5, 3), (7, 1, 5, 0), (5, 3, 5, 2), (4, 5, 3, 5), (5, 2, 5, 0), (3, 1, 1, 1), (5, 0, 4, 0), (1, 1, 1, 0), (1, 6, 0, 7), (7, 6, 6, 4), (2, 6, 3, 5), (6, 4, 4, 3), (4, 0, 7, 0), (5, 7, 4, 7), (7, 0, 4, 0), (4, 3, 6, 4), (4, 4, 5, 4), (5, 6, 4, 6), (4, 0, 5, 0), (6, 4, 5, 6), (0, 0, 0, 5), (1, 0, 1, 3), (3, 0, 4, 0), (1, 3, 2, 3), (5, 4, 6, 4), (2, 3, 2, 5), (0, 5, 0, 6), (4, 6, 3, 6), (5, 0, 5, 6), (2, 5, 2, 6), (4, 0, 5, 0), (2, 6, 2, 4), (5, 6, 4, 6), (3, 6, 2, 7)]
        state = recreate_state(state, move_seq)
        error_move = (4, 6, 4, 7)
        chess_board.print(state)
        print("Move causing error is {}".format(error_move))
        state = chess_board.get_state(state, error_move)


    def test_random_playouts(self):
        for i in range(100):
            state = chess_board.get_initial_state()
            move_history = []
            try:
                while not chess_board.ending_state(state):
                    legal_moves = chess_board.get_legal_moves(state)
                    random.shuffle(legal_moves)
                    move = legal_moves[0]
                    move_history.append(move)
                    state = chess_board.get_state(state, move)

                ending = chess_board.ending_state(state)
                if ending == -1:
                    print("Game ends in tie!")
                elif ending == 1:
                    print("Winner is {}!".format("White" if chess_board.get_player(state) != WHITE_PLAYER else "Black"))

            except Exception as e:
                print("\n\n!!!!!!\n!!!!Exception found during simulation.!!!!\n!!!!!!\n Move history {}".format(move_history))
            print("Game ended with state")
            chess_board.print(state)


def recreate_state(state, move_sequence):
    for move in move_sequence:
        state = chess_board.get_state(state, move)
    return state



def check_char(c):
    try:
        int(c)
        return True
    except ValueError:
        return False


def force_move(board, player, move):
    s_row, s_col, e_row, e_col = move
    board[e_row][e_col] = board[s_row][s_col]
    board[s_row][s_col] = EMPTY_SQUARE
    return chess_board.get_other_player(player)
