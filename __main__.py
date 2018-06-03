from game.ttt_game import TTTGame
import argparse


def main():
    parser = argparse.ArgumentParser(description='Play some games vs. AI')
    parser.add_argument("-s", "--searchtime", type=int, default=30, nargs='?',
                        help='thinking time for ai')
    parser.add_argument("-p", "--player", default=2, type=int, nargs='?',
                        help='human player (1 or 2)')

    args = parser.parse_args()
    searchtime = args.searchtime
    player = args.player
    # use parameters player=%1|2 and searchtime=%seconds
    # TTTGame(player=1, searchtime=10)
    game = TTTGame(searchtime=searchtime, player=player)
    game.start()


if __name__ == '__main__':
    main()
