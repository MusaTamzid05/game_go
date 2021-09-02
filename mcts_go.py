from dlgo import goboard
from dlgo import mcts


if __name__ == "__main__":
    BOARD_SIZE = 5
    game = goboard.GameState.new_game(BOARD_SIZE)
    bot = mcts.MCTSAgent(500, temparature = 1.4)
