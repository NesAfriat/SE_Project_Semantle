import os

import Semantle_AI.Business.Algorithms as Algo
import Semantle_AI.Business.Reports.GraphCalculator as Calc
import Semantle_AI.ModelComparator as Mc
from Semantle_AI.Business import MethodDistances
from Semantle_AI.Business.Reports.ReportsGenerator import generate_algo_guesses_from_csv
from Semantle_AI.Service.AgentHandlers.Agent1Handler import Agent1Handler
from Semantle_AI.Service.AgentHandlers.Agent2Handler import Agent2Handler
from Semantle_AI.Service.AgentHandlers.ManualAgentHandler import ManualAgentHandler
from Semantle_AI.Service.AgentHandlers.SmartAgent2Handler import SmartAgent2Handler

FASTTESXT_WIKI = "fasttext-wiki-news-subwords-300"  # 1GB
GLOVE_WIKI = "glove-wiki-gigaword-300"  # 376MB
WORD2VEC_RUSCORPORA = "word2vec-ruscorpora-300"  # 198MB
WORD2VEC_GOOGLE = "word2vec-google-news-300"  # 1.662GB
WORD2VEC = "Google_Word2Vec.bin"
WORDS_LIST = "words.txt"


class Menu:
    pca = None

    def __init__(self):
        self.concrete_agent_builder = None
        self.finished = False
        self.out = lambda *args: print(*args)

    def start_menu(self):
        done_loop = False
        while not self.finished and not done_loop:
            choose = self.busy_choose("Choose agent", "Agent1", "Agent2", "Smart agent 2", "Manual", "Generate a graph",
                                      "Exit")
            if choose == '1':
                self.concrete_agent_builder = Agent1Handler(self.out, input, self.finished)
                self.concrete_agent_builder.start_menu()
                self.start()
            elif choose == '2':
                self.concrete_agent_builder = Agent2Handler(self.out, input, self.finished)
                self.concrete_agent_builder.start_menu()
                self.start()
            elif choose == '3':
                self.concrete_agent_builder = SmartAgent2Handler(self.out, input, self.finished)
                self.concrete_agent_builder.start_menu()
                self.start_smart_play()
            elif choose == '4':
                self.concrete_agent_builder = ManualAgentHandler(self.out, input, self.finished)
                self.concrete_agent_builder.start_menu()
                self.start()
            elif choose == '5':
                self.generate_graphs()
            elif choose == '6':
                done_loop = True

    def start(self):
        self.concrete_agent_builder.get_result().start_play(self.out)

    def start_smart_play(self):
        self.concrete_agent_builder.get_result().start_play_with_priority(self.out)

    def generate_graphs(self):
        done_loop = False
        while not done_loop:
            choose = self.busy_choose("Choose the graph you want to create",
                                      "Export algorithms graph",
                                      "Create an algorithm graph",
                                      "Compare noise impact on the guesses number",
                                      "Compare noise impact on the guesses number using queue",
                                      "Load graph from files",
                                      "Compare two word models distances",
                                      "Compare different priority calculation",
                                      "Exit")
            if choose == '1':
                self.loop_times()
                done_loop = True
            elif choose == '2':
                self.one_algo_loop()
                done_loop = True
            elif choose == '3':
                self.noise_algo_loop()
            elif choose == '4':
                self.noise_algo_queue_loop()
            elif choose == '5':
                legal_path = False
                while not legal_path:
                    path = input("Enter full file path. The go back type \'Exit\'\n")
                    if path.lower() == 'exit':
                        done_loop = True
                    else:
                        if os.path.exists(path):
                            if "algorithms_compare" in path:
                                generate_algo_guesses_from_csv(path)
                            elif "algorithm_stat_" in path:
                                name = input("Enter file name.\n")
                                full_path = os.path.join(path, name)
                                Calc.show_png_file(full_path)
                        else:
                            print(f"The file path {path} does not exists.")
                        done_loop = True
            elif choose == '6':
                self.compare_models()
                done_loop = True
            elif choose == '7':
                self.compare_errors()
                done_loop = True
            elif choose == '8':
                done_loop = True

    def compare_models(self):
        models = (WORD2VEC, FASTTESXT_WIKI, GLOVE_WIKI, WORD2VEC_RUSCORPORA, WORD2VEC_GOOGLE)
        model1 = self.busy_choose("Choose Model", WORD2VEC, FASTTESXT_WIKI, GLOVE_WIKI, WORD2VEC_RUSCORPORA,
                                  WORD2VEC_GOOGLE)
        model2 = self.busy_choose("Choose Model", WORD2VEC, FASTTESXT_WIKI, GLOVE_WIKI, WORD2VEC_RUSCORPORA,
                                  WORD2VEC_GOOGLE)
        comparator = Mc.ModelComparator()
        comparator.create_models_graph(models[int(model1) - 1], models[int(model2) - 1])

    def compare_errors(self):
        models = (WORD2VEC, FASTTESXT_WIKI, GLOVE_WIKI, WORD2VEC_RUSCORPORA, WORD2VEC_GOOGLE)
        model1 = self.busy_choose("Choose The host model", WORD2VEC, FASTTESXT_WIKI, GLOVE_WIKI, WORD2VEC_RUSCORPORA,
                                  WORD2VEC_GOOGLE)
        model2 = self.busy_choose("Choose The second model", WORD2VEC, FASTTESXT_WIKI, GLOVE_WIKI, WORD2VEC_RUSCORPORA,
                                  WORD2VEC_GOOGLE)
        done_loop = False
        while not done_loop:
            print("=================== Number of games ===================\n\n")
            choose = input("Please type number of executions for the algorithm, to exit press \'e\'.\n")
            if choose.isnumeric():
                self.concrete_agent_builder = SmartAgent2Handler(input, self.out, self.finished)
                self.concrete_agent_builder.start_queue_loop(MethodDistances.cosine_function(), models[int(model1) - 1]
                                                             , models[int(model2) - 1])
                Calc.create_error_compare_graph(int(choose), self.concrete_agent_builder.get_result(),
                                                models[int(model1) - 1], models[int(model2) - 1])
                done_loop = True
            elif choose == 'e':
                done_loop = True
            else:
                print("Please choose a valid option")

    def loop_times(self):
        done_loop = False
        while not done_loop:
            print("=================== Number of games ===================\n\n")
            choose = input("Please type number of executions for each algorithm, to exit press \'e\'.\n")
            if choose.isnumeric():
                self.concrete_agent_builder = Agent2Handler(input, self.out, self.finished)
                self.concrete_agent_builder.start_loop_menu(MethodDistances.euclid_function())
                Calc.calculate_graph(int(choose), self.concrete_agent_builder.get_result())
                done_loop = True
            elif choose == 'e':
                done_loop = True
            else:
                print("Please choose a valid option")

    def noise_algo_loop(self):
        # setting the algo to run. For now hard coded as multi-lateration only.
        done_loop = False
        algo_dict = dict()
        algo_dict["Multi-Lateration"] = Algo.MultiLateration.MultiLateration(MethodDistances.euclid_function())

        # getting the number of runs to compare for each noise
        done = False
        while not done:
            print("=================== Dist func ===================\n\n")
            dist = input("Please type distance function.\n1.Euclidian.\n2.Cos function.\nTo exit press \'e\'.\n")
            if dist != '1' and dist != '2' and dist != 'e':
                print("Please enter a valid answer.")
                continue
            while not done_loop:
                print("=================== Number of games ===================\n\n")
                choose = input("Please type number of executions for the algorithm, to exit press \'e\'.\n")
                if choose.isnumeric():
                    if dist == '1':
                        self.concrete_agent_builder = Agent2Handler(input, self.out, self.finished)
                        self.concrete_agent_builder.start_loop_menu(MethodDistances.euclid_function())
                        Calc.calculate_noise_to_guesses_graph(int(choose), self.concrete_agent_builder.get_result(),
                                                              algo_dict, 'Euclid', withQueue=False)
                        done = True
                        done_loop = True
                    elif dist == '2':
                        self.concrete_agent_builder = Agent2Handler(input, self.out, self.finished)
                        self.concrete_agent_builder.start_loop_menu(MethodDistances.cosine_function())
                        Calc.calculate_noise_to_guesses_graph(int(choose), self.concrete_agent_builder.get_result(),
                                                              algo_dict, 'Cosin', withQueue=False)
                        done = True
                        done_loop = True
                    elif dist == 'e':
                        done_loop = True
                        done = True
                        continue
                elif choose == 'e':
                    done_loop = True
                else:
                    print("Please choose a valid option")

    def noise_algo_queue_loop(self):
        # setting the algo to run. For now hard coded as multi-lateration queue only.
        done_loop = False
        algo_dict = dict()
        # setting the smart multi-lateration agent.
        algo_dict["Multi-Lateration"] = Algo.MultiLaterationAgent2.SmartMultiLateration(
            MethodDistances.euclid_function())

        # getting the number of runs to compare for each noise
        done = False
        while not done:
            print("=================== Dist func ===================\n\n")
            dist = input("Please type distance function.\n1.Euclidian.\n2.Cos function.\nTo exit press \'e\'.\n")
            if dist != '1' and dist != '2' and dist != 'e':
                print("Please enter a valid answer.")
                continue
            while not done_loop:
                print("=================== Number of games ===================\n\n")
                choose = input("Please type number of executions for the algorithm, to exit press \'e\'.\n")
                if choose.isnumeric():
                    if dist == '1':
                        self.concrete_agent_builder = Agent2Handler(input, self.out, self.finished)
                        self.concrete_agent_builder.start_loop_menu(MethodDistances.euclid_function())
                        Calc.calculate_noise_to_guesses_graph(int(choose), self.concrete_agent_builder.get_result(),
                                                              algo_dict, 'Euclid', withQueue=True)
                        done = True
                        done_loop = True
                    elif dist == '2':
                        self.concrete_agent_builder = Agent2Handler(input, self.out, self.finished)
                        self.concrete_agent_builder.start_loop_menu(MethodDistances.cosine_function())
                        Calc.calculate_noise_to_guesses_graph(int(choose), self.concrete_agent_builder.get_result(),
                                                              algo_dict, 'Cosin', withQueue=True)
                        done = True
                        done_loop = True
                    elif dist == 'e':
                        done_loop = True
                        done = True
                        continue
                elif choose == 'e':
                    done_loop = True
                else:
                    print("Please choose a valid option")

    def one_algo_loop(self):
        done_loop1 = False
        done_loop2 = False
        algo_dict = dict()
        while not done_loop1:
            algorithm = self.busy_choose("Choose an algorithm to run", "Brute_force", "Multi_Lateration ",
                                         "Trilateration", "Exit")
            if algorithm == '1':
                algo_dict["Brute_force"] = Algo.Naive.Naive()
                done_loop1 = True
            elif algorithm == '2':
                algo_dict["Multi-Lateration"] = Algo.MultiLateration.MultiLateration(MethodDistances.euclid_function())
                done_loop1 = True
            elif algorithm == '3':
                algo_dict["Trilateration"] = Algo.NLateration.Trilateration()
                done_loop1 = True
            elif algorithm == '4':
                done_loop1 = True
                done_loop2 = True
                continue

        while done_loop1 and not done_loop2:
            choose = input("Please type number of executions for the algorithm, to exit press \'e\'.\n")
            if choose.isnumeric():
                self.concrete_agent_builder = Agent2Handler(input, self.out, self.finished)
                self.concrete_agent_builder.start_loop_menu(MethodDistances.euclid_function())
                Calc.calculate_algorithm_graph(int(choose), self.concrete_agent_builder.get_result(), algo_dict)
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
