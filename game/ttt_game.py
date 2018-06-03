from board.ttt import TTT
from mctsai.mcts import MCTS

class TTTGame():
    def __init__(self, **kwargs):
        self.search_time = kwargs.get("searchtime", 10)
        self.player = kwargs.get("player", 1)

    def start(self):
        ttt = TTT()
        mcts = MCTS(ttt, searchtime=self.search_time)
        state = mcts.root.state
        while not mcts.board.ending_state(state):
            if state[1] == self.player:
                print("\nYour move! Please wait while AI thinks...\n")
            else:
                print("\nAI's move! Please wait while AI thinks...\n")

            move = mcts.search()
            mcts.board.print(state)
            if state[1] == self.player:
                move = input("Make move! (format -> row col... e.g >>1 1)   \n>>").split(" ")
                if len(move) == 2:
                    move = (int(move[0]), int(move[1]))
                while move not in mcts.board.get_legal_moves(state):
                    move = input("Make move! (format -> row col... e.g >>1 1)   \n>>").split(" ")
                    if len(move) != 2:
                        continue
                    move = (int(move[0]), int(move[1]))

            mcts.make_move(move)
            state = mcts.root.state

        mcts.board.print(state)
