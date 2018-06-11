class Board(object):
    def __init__(self, **kwargs):
        return

    def get_initial_state(self):
        raise NotImplementedError

    def get_state(self, state, action):
        raise NotImplementedError

    def get_legal_moves(self, state):
        raise NotImplementedError

    def ending_state(self, state):
        raise NotImplementedError

    def get_player(self, state):
        raise NotImplementedError
