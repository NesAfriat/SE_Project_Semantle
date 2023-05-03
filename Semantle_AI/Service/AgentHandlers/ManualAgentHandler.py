from abc import ABC

from Semantle_AI.Business.Agents.ManualAgent import ManualAgent
from Semantle_AI.Service.AgentHandlers.AgentHandler import AgentHandler
from Semantle_AI.Business.MethodDistances import cosine_function

class ManualAgentHandler(AgentHandler):
    def on_online_mode(self):
        self.agent.set_agent_word2vec_model_online()

    def on_offline_mode(self):
        self.agent.set_host_model()

    def start_menu(self):
        host = self.busy_choose("\n choose your game type: \n", "offline", "online", "exit")
        if host == '1':
            self.create_offline_loop_host(cosine_function())
            self.agent.set_agent_word2vec_model()
            return True
        elif host == '2':
            self.create_online_host()
            self.agent.set_agent_word2vec_model()
            self.agent.set_host_model()
            return True
        else:
            return False


    def __init__(self, out, inp, finished):
        super().__init__(out, inp, finished)
        self.agent = ManualAgent()

    def start_loop_menu(self, dist):
        pass
