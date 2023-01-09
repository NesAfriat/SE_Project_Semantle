from Reports.GraphCalculator import calculate_graph
from Service.AgentMenu.Agent1Builder import Agent1Builder
from Service.AgentMenu.ManualAgentBuilder import ManualAgentBuilder


class Menu:
    pca = None

    def __init__(self):
        self.concrete_agent_builder = None
        self.finished = False
        self.out = lambda *args: print(*args)

    def start_menu(self):
        done_loop = False
        while not self.finished and not done_loop:
            choose = self.busy_choose("Choose agent", "Agent1", "Agent2", "Manual", "Export algorithms graph", "Exit")
            if choose == '1':
                self.concrete_agent_builder = Agent1Builder(self.out, input, self.finished)
                self.concrete_agent_builder.start_menu()
                self.start()
            elif choose == '2':
                self.concrete_agent_builder = Agent1Builder(self.out, input, self.finished)
                self.concrete_agent_builder.start_menu()
                self.start()
            elif choose == '3':
                self.concrete_agent_builder = ManualAgentBuilder(self.out, input, self.finished)
                self.concrete_agent_builder.start_menu()
                self.start()
            elif choose == '4':
                self.loop_times()
            elif choose == '5':
                done_loop = True

    def start(self):
        self.concrete_agent_builder.get_result().start_play(self.out)

    def loop_times(self):
        done_loop = False
        while not done_loop:
            choose = input("Please type number of executions for each algorithm, to exit press \'e\'.\n")
            if choose.isnumeric():
                self.concrete_agent_builder = Agent1Builder()
                self.concrete_agent_builder.start_loop_menu()
                calculate_graph(int(choose), self.concrete_agent_builder.get_result())
                done_loop = True
            elif choose == 'e':
                done_loop = True
            else:
                print("Please choose a valid option")

    def choose_agent(self):
        def choose_agent_model():
            choose = self.busy_choose(
                "Choose Agent Model", "Word2Vec")
            if choose == 'b':
                self.choose_agent()
            elif choose == '1':
                self.game_manager.create_agent1()
                self.game_manager.create_agent_word2vec_model_online()
                self.choose_algo()
            elif choose == 'e':
                self.finished = True

        ip = self.busy_choose("Choose Agent", "agent1", "agent2")
        if ip == 'b':
            self.human_or_AI_game()
        elif ip == '1':
            if self.offline_playing:
                self.game_manager.create_agent1()
                self.game_manager.set_agent_host_model()
                self.choose_algo()
            else:
                choose_agent_model()
        elif ip == '2':
            self.game_manager.create_agent1()
            choose_agent_model()
        elif ip == 'e':
            self.finished = True

    def busy_choose(self, to_write, *args):
        acc = ""
        num = 1
        for option in args:
            acc = acc + str(num) + ". " + option + "\n"
            num += 1
        num -= 1
        while True:
            ip = input("===================" + to_write + "===================\n\n" + acc)
            if ip == 'e' or ip == 'b' or (ip.isnumeric() and 0 < int(ip) <= num):
                return ip
            else:
                print("\nplease choose valid option please")

    def click_ok_and_start(self):
        input("\npress enter to start...  \n")
        self.concrete_agent_builder.get_result().start()

    def start_commandline_game(self):
        self.game_manager.start_human_game(input, lambda m: print(m))
