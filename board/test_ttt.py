from board.ttt import TTT
import unittest


class TestTTT(unittest.TestCase):
    def test_end(self):
        ttt = TTT()

        state = ttt.get_initial_state()
        ttt.print(state)
        self.assertFalse(ttt.ending_state(state))

        state = ttt.get_state(state, (0, 0))
        ttt.print(state)
        self.assertFalse(ttt.ending_state(state))

        state = ttt.get_state(state, (1, 0))
        ttt.print(state)
        self.assertFalse(ttt.ending_state(state))

        state = ttt.get_state(state, (1, 1))
        ttt.print(state)
        self.assertFalse(ttt.ending_state(state))

        state = ttt.get_state(state, (2, 0))
        ttt.print(state)
        self.assertFalse(ttt.ending_state(state))

        state = ttt.get_state(state, (2, 2))
        ttt.print(state)
        self.assertTrue(ttt.ending_state(state))
        self.assertFalse(ttt.get_legal_moves(state))








if __name__ == 'main':
    unittest.main()
