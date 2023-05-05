from Semantle_AI.Business.Agents.Agent import Agent
from Semantle_AI.Business.Algorithms.MultiLaterationAgent2 import SmartMultiLateration


class AgentPriority(Agent):

    def __init__(self):
        super().__init__()
        self.last_word = None

    def guess_word(self):
        self.last_word = self.algorithm.calculate()
        return self.last_word
    
    def calculateError(self):
        error = self.get_model().get_models_error(self.host.model, 2000)
        self.data.setError(error)

    def set_agent_smart_MultiLateration_algorithm(self):
        algo = SmartMultiLateration(self.data.model.dist_func)
        self.set_algorithm(algo, lambda: self.guess_n_queue_word(1))

    def set_host_model(self):
        self.set_model(self.host.model)