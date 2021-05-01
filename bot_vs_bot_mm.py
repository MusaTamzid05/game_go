from dlgo import goboard
from dlgo import gotypes
from dlgo.agent import minmax_agent
from dlgo.utils import print_board
from dlgo.utils import print_move
import time

def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)

    bots = {
            gotypes.Player.black : minmax_agent.MinimaxAgent(),
            gotypes.Player.white : minmax_agent.MinimaxAgent(),
            }


    while not game.is_over():
        time.sleep(0.3)
        print(chr(27) + "[2J")
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)






if __name__ == "__main__":
    main()
