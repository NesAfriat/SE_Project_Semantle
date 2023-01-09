from Business.Agents.ManualAgent import ManualAgent
from Service.AgentMenu.AgentBuilder import AgentBuilder


class ManualAgentBuilder(AgentBuilder):
    def start_menu(self):
        self.agent.set_agent_word2vec_model()


    def __init__(self, out, inp, finished):
        super().__init__(out, inp, finished)
        self.agent = ManualAgent()

