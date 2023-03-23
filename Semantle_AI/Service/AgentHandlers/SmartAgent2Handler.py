from Business.Agents.Agent2Priority import Agent2Priority
from Service.AgentHandlers.AgentHandler import AgentHandler


class SmartAgent2Handler(AgentHandler):
    def __init__(self, out, inp, finished):
        super().__init__(out, inp, finished)
        self.agent = Agent2Priority()

    def start_menu(self):
        self.choose_agent_2_host()
        self.choose_agent_model()
        self.choose_agent_2_algo()

    def start_loop_menu(self, dist):
        self.create_offline_loop_host(dist)
        self.agent.set_host_model()
        self.agent.set_agent_MultiLateration_algorithm()

    def start_queue_loop(self, dist, player_model):
        self.create_offline_loop_host(dist)
        self.agent.set_agent_model_from_url(player_model)
        self.agent.set_agent_smart_MultiLateration_algorithm()

    def on_offline_mode(self):
        pass

    def on_online_mode(self):
        pass
