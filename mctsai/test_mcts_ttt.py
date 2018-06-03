from board.ttt import TTT
from mctsai.mcts import Node
from mctsai.mcts import MCTS
import unittest

# 0 = self play
# 1 = human play
# 2 = block
# 3 = win
skip = [0, 2, 3]


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

    def test_selection(self):
        pass

    def test_playout(self):
        pass

    def test_back_prop(self):
        pass

    def test_expand(self):
        pass

    def test_block(self):
        if 2 in skip:
            print("Skipping test simple block")
            return
        ttt = TTT()
        state = ttt.get_initial_state()
        state = ttt.get_state(state, (1, 1))
        state = ttt.get_state(state, (2, 2))
        state = ttt.get_state(state, (2, 0))
        print("Testing simple block on the following board")
        ttt.print(state)
        for _ in range(1):
            mcts = MCTS(ttt)
            mcts.set_root_state(state)
            move = mcts.search()
            self.assertEqual(move, (0, 2))

    def test_simple_win(self):
        if 3 in skip:
            print("Skipping test simple win")
            return
        ttt = TTT()
        state = ttt.get_initial_state()
        state = ttt.get_state(state, (1, 1))
        state = ttt.get_state(state, (2, 2))
        state = ttt.get_state(state, (2, 0))
        state = ttt.get_state(state, (0, 2))
        state = ttt.get_state(state, (1, 2))
        state = ttt.get_state(state, (2, 1))
        print("Testing simple win on the following board")
        ttt.print(state)
        for _ in range(10):
            mcts = MCTS(ttt)
            mcts.set_root_state(state)
            while not mcts.board.ending_state(state):
                move = mcts.search()
                state = mcts.board.get_state(state, move)
                mcts.board.print(state)
                mcts.make_move(move)
            mcts.board.print(state)

            # self.assertEqual(move, (0, 2))

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






