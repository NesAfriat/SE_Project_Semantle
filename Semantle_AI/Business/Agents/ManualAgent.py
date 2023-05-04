from Semantle_AI.Business.Agents.Agent import Agent
from copy import copy


class ManualAgent(Agent):

    def guess_word(self):
        pass

    def set_host_model(self):
        self.set_model(self.host.model)


