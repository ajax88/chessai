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

    def ucb1_child(self):
        return max(self.children, key=lambda c: (c.wins / c.total_visits) + math.sqrt(2) * math.sqrt(math.log(self.total_visits) / c.total_visits))

    # Used as a value function for best move once simulation is complete
    def eval(self):
        return (self.total_visits - self.wins) / self.total_visits


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
        best_child = self.select()
        if best_child.remaining_moves:
            new_discovered_node = self.expand(best_child)
            result = self.playout(new_discovered_node)
            self.back_propagate(result, new_discovered_node)

    def back_propagate(self, result, node):
        cp_node = node
        while cp_node:
            cp_node.update(result)
            if result == 1:
                result = 0
            elif result == 0:
                result = 1
            # result *= -1 # switch result based on change of player... decay old results?
            cp_node = cp_node.parent

    def playout(self, node):
        state = node.state
        start_player = state[1]
        while not self.board.ending_state(state):
            action = self.sample_action(state)
            state = self.board.get_state(state, action)

        # if result is 1, the opposite player of the current state has won
        if self.board.ending_state(state) == 1:
            return 1 if start_player != state[1] else 0
        return 0.5

    def expand(self, node):
        curr_state = node.state
        action = node.remaining_moves.pop()
        new_state = self.board.get_state(curr_state, action)
        new_node = Node(from_action=action, state=new_state, remaining_moves=self.board.get_legal_moves(new_state), parent=node)
        random.shuffle(new_node.remaining_moves)
        node.children.append(new_node)
        return new_node

    def search(self):
        end_time = datetime.datetime.now() + self.stime
        print("Starting MCTS search...")
        search_count = 0
        try:
            while datetime.datetime.now() < end_time:
                self.simulate()
                self.simulations += 1
                search_count += 1
                if search_count % 5000 == 0:
                    print("Searching{}".format("." * (search_count // 5000)))
            print("Search time complete. {} simulations ran.".format(search_count))
        except SimulationComplete as sc:
            print(sc)

        return self.find_move()

    def find_move(self):
        max_node = max(self.root.children, key=lambda node: node.eval())
        return max_node.from_action

    def select(self):
        curr = self.root
        while not curr.remaining_moves: # while fully expanded
            if self.board.ending_state(curr.state):
                curr.visited = True
                break

            available_paths = list(filter(lambda n: not n.visited, curr.children))
            if not available_paths:
                curr.visited = True
                if curr.parent is None: # root
                    raise SimulationComplete("All paths explored")
                break

            curr = curr.ucb1_child()
        return curr

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
