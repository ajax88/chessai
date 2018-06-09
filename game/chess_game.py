from board.chessboard import ChessBoard
from mctsai.mcts import MCTS

class ChessGame():
    def __init__(self, **kwargs):
        self.search_time = kwargs.get("searchtime", 10)
        self.player = kwargs.get("player", 1)
        self.debug = kwargs.get("debug", False)

    def start(self):
        chess = ChessBoard(debug=self.debug)
        mcts = MCTS(chess, searchtime=self.search_time)
        state = chess.get_initial_state()
        # Implement turn logic here
        chess.print(state)
