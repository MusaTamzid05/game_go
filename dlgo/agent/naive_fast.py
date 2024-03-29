from dlgo.agent.base import Agent
from dlgo.gotypes import Point
from dlgo.goboard import Move
from dlgo.helpers import is_point_an_eye
import numpy as np

class FastRandomBot(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.dim = None
        self.point_cache = []

    def _update_cache(self, dim):
        '''
        Intialize the list from the given dim.
        '''
        self.dim = dim
        rows, cols = dim
        self.point_cache = []

        for r in range(1, rows + 1):
            for c in range(1, cols + 1):
                self.point_cache.append(Point(row = r, col = c))


    def select_move(self, game_state):
        dim = (game_state.board.num_rows, game_state.board.num_cols)

        if dim != self.dim:
            self._update_cache(dim)

        idx = np.arange(len(self.point_cache))
        np.random.shuffle(idx)

        for i in idx:
            p = self.point_cache[i]

            # is valid move, return

            if game_state.is_valid_move(Move.play(p)) and not is_point_an_eye(game_state.board,
                    p, game_state.next_player):
                return Move.play(p)

        return Move.pass_turn()
