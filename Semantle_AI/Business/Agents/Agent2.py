from Business.Agents.Agent import Agent


class Agent2(Agent):

    def __init__(self):
        super().__init__()
        self.last_word = None

    def guess_word(self, *args):
        self.last_word = self.algorithm.calculate(*args)
        return self.last_word
