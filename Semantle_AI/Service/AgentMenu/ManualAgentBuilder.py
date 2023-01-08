from Business.Agents.ManualAgent import ManualAgent
from Service.AgentMenu.AgentBuilder import AgentBuilder


class ManualAgentBuilder(AgentBuilder):
    def start_menu(self):
        pass

    def __init__(self, out, inp, finished):
        super().__init__(out, inp, finished)
        self.agent = ManualAgent()

