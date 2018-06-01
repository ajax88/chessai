import datetime

class Node(object):
    def __init__(self, **kwargs):
        self.state = kwargs.get('state', None)
        self.player = kwargs.get('player', None)
        self.wins = kwargs.get('wins', 0)
        self.total_visits = kwargs.get('total_visits', 0)
        self.parent = kwargs.get('parent', None)
        self.children = []

    def update(self, result):
        if result == 1:
            self.wins += 1
        self.total_visits += 1


class MCTS(object):
    def __init__(self, board, **kwargs):
        self.board = board
        self.root = kwargs.get("root", Node())
        if not self.root.state:
            self.root.state = self.board.get_initital_state()
        self.stime = datetime.timedelta(seconds=kwargs.get('search_time', 30))

    def simulate(self):
        best_child = self.selection()
        new_discovered_node = self.expand(best_child)
        result = self.playout(new_discovered_node)
        self.back_propagate(result, new_discovered_node)

    def back_propagate(self, result, node):
        cp_node = node
        while cp_node:
            cp_node.update(result)
            result *= -1  # switch result based on change of player
            cp_node = cp_node.parent

    def playout(self, node):
        pass

    def expand(self, node):
        pass

    def search(self):
        end_time = datetime.datetime.now() + self.stime
        simulations = 0
        print("Starting MCTS search...")
        while datetime.datetime.now() < end_time:
            self.simulate()
            simulations += 1
        print("Search time complete. {} simulations ran.".format(simulations))
        return self.find_move()

    def find_move(self):
        return max(self.root.children, key=lambda node: node.total_visits)

    def selection(self):
        return Node()


