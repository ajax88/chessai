from game.ttt_game import TTTGame


def main():
    # use parameters player=%1|2 and searchtime=%seconds
    # TTTGame(player=1, searchtime=10)
    game = TTTGame(searchtime=30, player=2)
    game.start()


if __name__ == '__main__':
    main()
