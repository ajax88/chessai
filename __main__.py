from game.ttt_game import TTTGame
from game.chess_game import ChessGame
import argparse


def main():
    parser = argparse.ArgumentParser(description='Play some games vs. AI')
    parser.add_argument("-s", "--searchtime", type=int, default=30, nargs='?',
                        help='thinking time for ai')
    parser.add_argument("-p", "--player", default=2, type=int, nargs='?',
                        help='human player (1 or 2)')
    parser.add_argument("-g", "--game", default='ttt', type=str, nargs='?',
                        help='which game to play (chess or ttt)')
    parser.add_argument("-d", "--debug", default=False, type=bool, nargs='?',
                        help='enable debug mode')
    parser.add_argument("-x", "--self_play", default=False, type=bool, nargs='?',
                        help='enable self play mode')

    args = parser.parse_args()
    searchtime = args.searchtime
    player = args.player
    game_type = args.game
    debug = args.debug
    self_play = args.self_play
    # use parameters player=%1|2 and searchtime=%seconds
    # TTTGame(player=1, searchtime=10)
    if game_type == 'ttt':
        game = TTTGame(searchtime=searchtime, player=player)
    elif game_type == 'chess':
        game = ChessGame(searchtime=searchtime, player=player, debug=debug, self_play=self_play)

    game.start()


if __name__ == '__main__':
    main()
