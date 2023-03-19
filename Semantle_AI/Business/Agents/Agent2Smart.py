from Business.Agents.Agent import Agent
from Business.Algorithms.MultiLateration import MultiLateration


class Agent2(Agent):

    def __init__(self):
        super().__init__()
        self.last_word = None

    def guess_word(self):
        self.last_word = self.algorithm.calculate()
        return self.last_word
    
    def calculateError(self):
        error = self.get_model().get_models_error(self.host.model, 2000)
        self.data.set_error(error)

    def set_agent_MultiLateration_algorithm(self):
        algo = MultiLateration(self.data.model.dist_func)
        self.set_algorithm(algo, self.guess_n_random_word(1))
