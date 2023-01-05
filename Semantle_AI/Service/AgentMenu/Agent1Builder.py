from Business.Agents.Agent1 import Agent1
from Service.AgentMenu.AgentBuilder import AgentBuilder


class Agent1Builder(AgentBuilder):
    def start_menu(self):
        self.step_A()

    def __init__(self, out, inp, finished):
        super().__init__(out, inp, finished)
        self.agent = Agent1()

    def step_A(self):
        def choose_host():
            prev_menu = False
            while not self.finished and not prev_menu:
                off_on = self.busy_choose(
                    "Choose offline or online Host", "offline.", "online")
                if off_on == '1':
                    self.create_offline_host()
                    self.agent.set_host_model()
                    self.step_B()
                    prev_menu = True
                elif off_on == '2':
                    self.create_online_host()
                    self.agent.set_agent_word2vec_model_online()
                    self.step_B()
                    prev_menu = True
                elif off_on == 'e':
                    self.finished = True
                elif off_on == 'b':
                    prev_menu = True

        choose_host()

    def step_B(self):
        def choose_algo():
            prev_menu = False
            while not self.finished and not prev_menu:
                ip = self.busy_choose("Choose Algorithm", "Naive", "BruteForce", "Trilateraion")
                if ip == 'b':
                    prev_menu = True
                elif ip == '1':
                    self.agent.set_agent_naive_algorithm()
                    prev_menu = True
                elif ip == '2':
                    self.agent.set_agent_Brute_Force_algorithm()
                    prev_menu = True
                elif ip == '3':
                    self.agent.set_agent_trilateration_algorithm()
                    prev_menu = True
                elif ip == 'e':
                    self.finished = True
        choose_algo()
