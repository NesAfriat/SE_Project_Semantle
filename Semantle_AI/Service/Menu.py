from Business.Reports.GraphCalculator import calculate_graph, calculate_algorithm_graph
from Service.AgentHandlers.Agent1Handler import Agent1Handler
from Service.AgentHandlers.Agent2Handler import Agent2Handler
from Service.AgentHandlers.ManualAgentHandler import ManualAgentHandler
import Business.Algorithms as algo
from Business import MethodDistances

class Menu:
    pca = None

    def __init__(self):
        self.concrete_agent_builder = None
        self.finished = False
        self.out = lambda *args: print(*args)

    def start_menu(self):
        done_loop = False
        while not self.finished and not done_loop:
            choose = self.busy_choose("Choose agent", "Agent1", "Agent2", "Manual", "Export algorithms graph","Crate an algorithm graph", "Exit")
            if choose == '1':
                self.concrete_agent_builder = Agent1Handler(self.out, input, self.finished)
                self.concrete_agent_builder.start_menu()
                self.start()
            elif choose == '2':
                self.concrete_agent_builder = Agent2Handler(self.out, input, self.finished)
                self.concrete_agent_builder.start_menu()
                self.start()
            elif choose == '3':
                self.concrete_agent_builder = ManualAgentHandler(self.out, input, self.finished)
                self.concrete_agent_builder.start_menu()
                self.start()
            elif choose == '4':
                self.loop_times()
            elif choose == '5':
                self.one_algo_loop()
            elif choose == '6':
                done_loop = True

    def start(self):
        self.concrete_agent_builder.get_result().start_play(self.out)

    def loop_times(self):
        done_loop = False
        while not done_loop:
            choose = input("Please type number of executions for each algorithm, to exit press \'e\'.\n")
            if choose.isnumeric():
                self.concrete_agent_builder = Agent1Handler(input, self.out, self.finished)
                self.concrete_agent_builder.start_loop_menu()
                calculate_graph(int(choose), self.concrete_agent_builder.get_result())
                done_loop = True
            elif choose == 'e':
                done_loop = True
            else:
                print("Please choose a valid option")

    def one_algo_loop(self):
        done_loop1 = False
        done_loop2 = False
        algo_dict = dict()
        while not done_loop1:
            algorithm = self.busy_choose("Choose an algorithm to run", "Brute_force", "Multi_Lateration ", "Trilateration",  "Exit")
            if algorithm == '1':
                algo_dict["Brute_force"] = algo.Naive.Naive()
                done_loop1 = True
            elif algorithm == '2':
                algo_dict["Multi-Lateratio"] = algo.MultiLateration.MultiLateration(MethodDistances.euclid_function())
                done_loop1 = True
            elif algorithm == '3':
                algo_dict["Trilateration"] = algo.NLateration.Trilateration()
                done_loop1 = True
            elif algorithm == '4':
                done_loop1 = True
                done_loop2 = True
                continue

        while done_loop1 and not done_loop2:
            choose = input("Please type number of executions for the algorithm, to exit press \'e\'.\n")
            if choose.isnumeric():
                self.concrete_agent_builder = Agent1Handler(input, self.out, self.finished)
                self.concrete_agent_builder.start_loop_menu()
                calculate_algorithm_graph(int(choose), self.concrete_agent_builder.get_result(), algo_dict)
                done_loop2 = True
            elif choose == 'e':
                done_loop2 = True
            else:
                print("Please choose a valid option")


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
