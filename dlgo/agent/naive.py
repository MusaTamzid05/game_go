from dlgo.agent.base import Agent
from dlgo.gotypes import Point
from dlgo.goboard import Move
from dlgo.helpers import is_point_an_eye
import random

class RandomBot(Agent):

    def select_move(self, game_state):
        candidates = []

        # select all the valid moves

        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.board.num_cols + 1):
                candidate = Point(row = r, col = c)
                if game_state.is_valid_move(Move.play(candidate)) and not  is_point_an_eye(game_state.board,
                        candidate,
                        game_state.next_player):
                    candidates.append(candidate)

                if not candidates:
                    return Move.pass_turn()

        # select a move randomly.

        return Move.play(random.choice(candidates))


