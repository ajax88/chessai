from board.ttt import TTT
from mctsai.mcts import MCTS
import unittest

# skip = [0, 1]

skip = [0]

class TestTTT(unittest.TestCase):
    def test_mcts(self):
        if 0 in skip:
            print("Skipping ai self-play")
            return
        ttt = TTT()
        for i in range(1000):
            mcts = MCTS(ttt)
            state = mcts.root.state
            while not mcts.board.ending_state(state):
                move = mcts.search()
                print(move)
                state = mcts.board.get_state(state, move)
                mcts.board.print(state)
                mcts.make_move(move)
            self.assertEqual(mcts.board.ending_state(state), -1)

    def test_play_mcts(self):
        if 1 in skip:
            print("Skipping human-ai play")
            return

        ttt = TTT()
        mcts = MCTS(ttt)
        state = mcts.root.state
        my_player = 2
        while not mcts.board.ending_state(state):
            mcts.board.print(state)
            move = mcts.search()
            print(move)
            if state[1] == my_player:
                move = input("Make move!\n")
                move = (int(move[0]), int(move[1]))

            mcts.make_move(move)
            state = mcts.root.state
        mcts.board.print(state)
            # state = mcts.board.get_state(state, move)
            # mcts = MCTS(ttt)
            # mcts.root.state = state
            # mcts.root.remaining_moves = mcts.board.get_legal_moves(mcts.root.state)

    def test_positions(self):
        # simple block
        move_sequence = [(1, 1), (2, 0), (0, 1)]
        # self.from_position(move_sequence, (2, 1), "Simple block 1")

        # simple block 2
        move_sequence = [(1, 1), (2, 2), (2, 1)]
        # self.from_position(move_sequence, (0, 1), "Simple block 2")

        # simple win 1
        move_sequence = [(1, 1), (2, 2), (2, 0), (0, 2), (1, 2), (2, 1)]
        # self.from_position(move_sequence, (1, 0), "Simple win")

    def from_position(self, move_sequence, expected_move, name):
        ttt = TTT()
        mcts = MCTS(ttt, searchtime= 30)
        mcts.board.print(mcts.root.state)
        for move in move_sequence:
            mcts.search()
            mcts.make_move(move)
            mcts.board.print(mcts.root.state)

        move = mcts.search()

        print("Testing {} block (that was lost before) on the following board".format(name))
        self.assertEqual(move, expected_move)

    def test_trick_win(self):
        pass
        # ttt = TTT()
        # state = ttt.get_initial_state()
        # state = ttt.get_state(state, (1, 1))
        # state = ttt.get_state(state, (2, 2))
        # state = ttt.get_state(state, (2, 0))
        # print("Testing trick win on the following board")
        # ttt.print(state)
        # for _ in range(100):
        #     mcts = MCTS(ttt)
        #     mcts.set_root_state(state)
        #     move = mcts.search()
        #     self.assertEqual(move, (0, 2))

    def test_defend_trick_win(self):
        pass






