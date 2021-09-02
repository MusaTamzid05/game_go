from dlgo.agent.base import Agent


class MCTSAgent(Agent):
    def __init__(self, num_rounds, temparature):
        Agent.__init__(self)
        self.num_rounds = num_rounds
        self.temparature = temparature

    def select_move(self, game_state):
        exit(1)

