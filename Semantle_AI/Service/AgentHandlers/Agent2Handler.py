from Business.Agents.Agent2 import Agent2
from Service.AgentHandlers.AgentHandler import AgentHandler


class Agent2Handler(AgentHandler):
    def __init__(self, out, inp, finished):
        super().__init__(out, inp, finished)
        self.agent = Agent2()

    def start_menu(self):
        self.choose_agent_model()
        self.choose_host()
        self.choose_algo()


    def on_offline_mode(self):
        pass

    def on_online_mode(self):
        pass
