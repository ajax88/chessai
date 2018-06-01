from board.board import Board

# ttt state (board, player)
class TTT(Board):
    def __init__(self):
        super().__init__()

    def get_initial_state(self):
        board = [[' ' for _ in range(3)] for _ in range(3)]
        return board, 1

    def get_state(self, state, action):
        board, player = state
        i, j = action
        board[i][j] = self.get_player_icon(player)

    def get_legal_moves(self, state):
        board, player = state
        moves = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    moves.append((i, j))
        return moves

    def get_enumerations(self, board):
        enumerated = []
        diag1 = []
        diag2 = []
        for i in range(3):
            diag1 += board[i][i]
            diag2 += board[2 - i][i]
            enumerated.append(board[i]) # row
            col = []
            for j in range(3):
                col.append(board[j][i])
            enumerated.append(col)
        enumerated.append(diag1)
        enumerated.append(diag2)

        return enumerated

    def ending_state(self, state):
        board, curr = state
        enumerated = self.get_enumerations(board)

        return any(self.check_three(s, self.opposite(curr)) for s in enumerated)


    def check_three(self, three, icon):
        return all(square is icon for square in three)

    def get_player_icon(self, player):
        return 'O' if player == 1 else 'X'

    def opposite(self, player):
        return 2 if player == 1 else 1


