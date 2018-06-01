from board.ttt import TTT


def main_test():
    ttt = TTT()
    state = ttt.get_initial_state()
    board, _ = state

    print(ttt.get_enumerations(board))


main_test()
