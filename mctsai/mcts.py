import datetime
import math
import random


class Node(object):
    def __init__(self, **kwargs):
        self.state = kwargs.get("state", None)
        self.from_action = kwargs.get("from_action", None)
        self.remaining_moves = kwargs.get("remaining_moves", None)
        self.wins = kwargs.get('wins', 0)
        self.total_visits = kwargs.get('total_visits', 0)
        self.parent = kwargs.get('parent', None)
        self.children = []
        self.visited = False

    def update(self, result):
        self.wins += result
        self.total_visits += 1

    def child_ucb1(self):
        r = list(filter(lambda c: not c.visited, self.children))
        return max(r, key=lambda c: (c.wins / c.total_visits) + math.sqrt(2) * math.sqrt(math.log(self.total_visits) / c.total_visits))

    # used as value function for move selection after simulations
    def eval(self):
        return self.total_visits


class MCTS(object):
    def __init__(self, board, **kwargs):
        self.simulations = 0
        self.board = board
        self.root = kwargs.get("root", Node())
        if not self.root.state:
            self.root.state = self.board.get_initial_state()
        self.root.remaining_moves = self.board.get_legal_moves(self.root.state)
        self.stime = datetime.timedelta(seconds=kwargs.get('searchtime', 30))

    def simulate(self):
        best_child = self.selection(self.root)
        new_discovered_node = self.expand(best_child)
        result = self.playout(new_discovered_node)
        self.back_propagate(result, new_discovered_node)

    def back_propagate(self, result, node):
        cp_node = node
        while cp_node:
            cp_node.update(result)
            result *= -1 # switch result based on change of player... decay old results?
            cp_node = cp_node.parent

    def playout(self, node):
        state = node.state
        start_player = state[1]
        while not self.board.ending_state(state):
            action = self.sample_action(state)
            state = self.board.get_state(state, action)

        # if result is 1, the opposite player of the current state has won
        if self.board.ending_state(state) == 1:
            return 1 if start_player != state[1] else -1
        return 0

    def expand(self, node):
        curr_state = node.state
        random.shuffle(node.remaining_moves)
        action = node.remaining_moves.pop()
        new_state = self.board.get_state(curr_state, action)
        new_node = Node(from_action=action, state=new_state, remaining_moves=self.board.get_legal_moves(new_state), parent=node)
        node.children.append(new_node)
        return new_node

    def search(self):
        end_time = datetime.datetime.now() + self.stime
        print("Starting MCTS search...")
        try:
            while datetime.datetime.now() < end_time:
                self.simulate()
                self.simulations += 1
                if self.simulations % 5000 == 0:
                    print("Searching{}".format("." * (self.simulations // 5000)))
            print("Search time complete. {} simulations ran.".format(self.simulations))
        except SimulationComplete as sc:
            print(sc)

        self.simulations = 0
        return self.find_move()

    def find_move(self):
        max_node = max(self.root.children, key=lambda node: node.eval())
        return max_node.from_action

    def selection(self, node):
        curr = node
        if curr.remaining_moves:
            return curr

        if self.board.ending_state(curr.state):
            curr.visited = True
            return self.selection(curr.parent)

        available_paths = list(filter(lambda n: not n.visited, curr.children))
        if not available_paths:
            curr.visited = True
            if curr.parent is None: # root
                raise SimulationComplete("All paths explored")
            return self.selection(curr.parent)

        curr = curr.child_ucb1()
        return self.selection(curr)

    def ucb1(self, node):
        # wins = node.wins if not flip_wins else node.total_visits - node.wins
        wins = node.total_visits - node.wins
        total_visits = node.total_visits
        return (wins / total_visits) + math.sqrt(2) * math.sqrt(math.log(total_sim, math.e) / total_visits)

    def sample_action(self, state):
        legal_moves = self.board.get_legal_moves(state)
        # randint returns random int inclusive of range [a, b]
        rand_index = random.randint(0, len(legal_moves) - 1)
        return legal_moves[rand_index]

    def make_move(self, action):
        new_node = list(filter(lambda node: node.from_action == action, self.root.children))[0]
        self.root = new_node
        self.root.parent = None

    def set_root_state(self, state):
        self.root.state = state
        self.root.remaining_moves = self.board.get_legal_moves(state)


class SimulationComplete(Exception):
    pass

## TODO : QUESTIONS TO ADDRESS ... is it right to flip wins...? maybe use negative
## TODO : UCB may be wrong. total wins? not parent?
