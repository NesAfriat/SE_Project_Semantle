from Semantle_AI.Business.Agents.Agent import Agent
from Semantle_AI.Service.AgentHandlers.AgentHandler import AgentHandler


class Agent1Handler(AgentHandler):

    def set_agent_model_offline(self):
        self.agent.set_host_model()

    def on_online_mode(self):
        self.agent.set_agent_word2vec_model_online()

    def on_offline_mode(self):
        self.agent.set_host_model()

    is_offline = True

    def start_menu(self):
        self.choose_host()
        self.choose_algo()

    def start_loop_menu(self, dist):
        self.create_offline_loop_host(dist)
        self.agent.set_host_model()
        self.agent.set_agent_smart_MultiLateration_algorithm()

    def __init__(self, out, inp, finished):
        super().__init__(out, inp, finished)
        self.agent = Agent()
