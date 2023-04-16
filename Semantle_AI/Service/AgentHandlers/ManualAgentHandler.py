from abc import ABC

from Business.Agents.ManualAgent import ManualAgent
from Service.AgentHandlers.AgentHandler import AgentHandler


class ManualAgentHandler(AgentHandler, ABC):
    def start_menu(self):
        self.agent.set_agent_word2vec_model()

    def __init__(self, out, inp, finished):
        super().__init__(out, inp, finished)
        self.agent = ManualAgent()

    def start_loop_menu(self, dist):
        pass
