from board.chessboard import ChessBoard
from mctsai.mcts import MCTS
from board.test_chess import check_char

class ChessGame():
    def __init__(self, **kwargs):
        self.search_time = kwargs.get("searchtime", 10)
        self.player = kwargs.get("player", 1)
        self.debug = kwargs.get("debug", False)
        self.self_play = kwargs.get("self_play", True)

    def start(self):
        if self.self_play:
            self.play_self()
        else:
            chess = ChessBoard(debug=self.debug)
            mcts = MCTS(chess, searchtime=self.search_time)
            state = chess.get_initial_state()
            # Implement turn logic here
            chess.print(state)

    def play_self(self):
        chess_board = ChessBoard(debug=self.debug)
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
            print("\n\n\n!!!!\n!!!!!!!Exception occurred.!!!!!!!\n!!!!\n\n Move history:\n".format(move_history))
