import sample.helpers.constants


class Board(object):
    #               INITIALIZATION METHODS

    def __init__(self, row, col):
        self.board = [[sample.helpers.constants.BLANK for _ in range(row)] for _ in range(col)]
        self.row = row
        self.col = col

    #               PUBLIC METHODS

    def get_square(self, row, col):
        if row >= self.row or row < 0 or col >= self.col or col < 0:
            raise ValueError('Index out of bounds {}, {}'.format(row, col))
        return self.board[row][col]

    def set_square(self, row, col, c):
        if row >= self.row or row < 0 or col >= self.col or col < 0:
            raise ValueError('Index out of bounds {}, {}'.format(row, col))

        self.board[row][col] = c


# PRINTING METHODS
'''
    def print(self):
        print(self)

    def __str__(self):
        my_str = ''
        for row in self.board:
            for _ in range(self.row):
                my_str += ' -'
            my_str += '\n'
            my_str += '|'
            for c in row:
                my_str += c
                my_str += '|'
            my_str += '\n'
        for _ in range(self.row):
            my_str += ' -'
        return my_str
'''
