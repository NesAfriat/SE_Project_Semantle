from collections import OrderedDict
import Semantle_AI.Business.Reports.ReportsGenerator as Reporter
import Semantle_AI.Business.Algorithms as Alg
from Semantle_AI.Business import MethodDistances
from Semantle_AI.Business.Agents.Agent import Agent
from Semantle_AI.Business.Algorithms import MultiLaterationAgent2
from Semantle_AI.Business.Reports.Calculator import Calculator
import matplotlib.pyplot as plt
import os

WORDS_LIST = "word_list.txt"
WORD2VEC = "Google_Word2Vec.bin"
DISTANCE_METHOD = "Euclid"


def select_words(num_of_words, vocab):
    ret = set()
    while len(ret) < num_of_words:
        if len(vocab) == 0:
            raise ValueError("Not enough words in the vocabulary to run.")
        to_add = vocab.pop()
        if to_add not in ret:
            ret.add(to_add)
    return ret


def load_words_list():
    path = os.path.join(os.getcwd(), "Business", "Reports", WORDS_LIST)
    try:
        with open(path, 'r') as file:
            lines = [line.strip() for line in file]
        return lines
    except FileNotFoundError:
        print(f"Error: {path} does not exist.")
        return []


def save_words_list(words_list):
    path = os.path.join(os.getcwd(), "Business", "Reports", WORDS_LIST)
    with open(path, 'w') as file:
        file.truncate(0)
        file.write('\n'.join(words_list))


def calculate_graph(runs_number, agent: Agent):
    # select the 'runs_number' words that will be run on each algorithm.
    words_list = select_words(runs_number, agent.get_vocab())
    algo_dict = dict({"Brute_force": Alg.Naive.Naive(),
                      "Multi-Lateration ": Alg.MultiLateration.MultiLateration(MethodDistances.euclid_function()),
                      "Trilateration": Alg.NLateration.Trilateration()})

    # init the result
    # for each algo, run all words.
    for counter, (algo_name, algorithm) in enumerate(algo_dict.items(), 1):
        setAgentAlgo(type(algorithm), agent)

        # init the statistics result for the algorithm
        calculator = Calculator()

        # iterate over each word and run the game
        for word in words_list:

            # setting the secret word in each session.
            agent.set_secret_word(word)
            agent.start_play(lambda args: args)

            # after run finished, collect the data.
            statistics = agent.get_statistics()
            for key in statistics:
                calculator.add_result(key, statistics[key])
            agent.reset_data()

        # After creating average
        k = calculator.calc_avg()
        for key, res in k.items():
            if key == list(k.keys())[-1]:
                Reporter.save_guess_data(counter, key, 0)
            else:
                Reporter.save_guess_data(counter, key, res)

        Reporter.save_game_data(counter, WORD2VEC, WORD2VEC, algo_name, DISTANCE_METHOD)

    path = Reporter.generate_data_files()
    Reporter.generate_algo_guesses_from_csv(path)


algo_dict = dict({"naive": Alg.Naive.Naive(),
                  "multi-lateration": Alg.MultiLateration.MultiLateration(MethodDistances.euclid_function()),
                  "n-lateration": Alg.NLateration.Trilateration()})


def calculate_algorithm_graph(runs_number, agent: Agent, algos_list):
    # select the 'runs_number' words that will be run on each algorithm.
    words_list = select_words(runs_number, agent.get_vocab())

    # init the result
    # for each algo, run all words.
    for algo_name in algos_list:

        setAgentAlgo(type(algo_dict[algo_name]), agent)

        # initialize the statistics result for the algorithm
        calculator = Calculator()

        # iterate over each word and run the game
        for word in words_list:

            # setting the secret word in each session.
            agent.set_secret_word(word)
            agent.start_play(lambda args: args)

            # after run finished, collect the data.
            statistic = agent.get_statistics()

            # get the last guess and remaining words after it
            last_guess = max(statistic.keys())
            # remaining_words = statistic[last_guess]

            # add the result to the calculator
            calculator.add_error_result(last_guess)

            # reset the agent's data
            agent.reset_data()

        # After the data setting, Creating average of the results in calculator.
        Reporter.generate_graph(calculator.results.keys(), algo_name, runs_number)


def calculate_noise_to_guesses_graph(runs_number, agent: Agent, algos_list, dist_name, withQueue):
    # select the noises for each run.
    noises_list = [1.06]
    if withQueue:
        agent.data.is_priority = True
    # select the 'runs_number' words that will be run on each algorithm.
    words_list = load_words_list()
    if len(words_list) == 0 or len(words_list) != runs_number:
        words_list = select_words(runs_number, agent.get_vocab())
        save_words_list(words_list)

    # for each algo, run all words.
    for algo_name in algos_list:
        # get the algo class
        setAgentAlgo(type(algo_dict[algo_name]), agent)

        # init the statistics result for the algorithm
        calculator = Calculator()

        # run each word with each noise
        for noise in noises_list:
            # setting the runs current error.
            agent.data.error = noise
            # iterate over each word and run the game
            for word in words_list:
                # setting the secret word in each session.
                agent.set_secret_word(word)

                agent.start_play(lambda args: args)

                # after run finished, collect the data.
                statistic = agent.get_statistics()

                # get the last guess and remaining words after it
                last_guess = max(statistic.keys())

                # add the result to the calculator
                calculator.add_noise_result(noise, last_guess, word)

                # reset the agent's data
                agent.reset_data()

        # After the data setting, Creating average of the results in calculator.
        Reporter.generate_noises_graph_spread(calculator.results, algo_name, runs_number, dist_name, withQueue)


def create_error_compare_graph(runs_number, agent: Agent, model1_name, model2_name, error, error_method,
                               error_size_method):
    # setting the statistics to be by the priority heap and not remain words.
    agent.data.is_priority = True
    agent.data.setError(error)
    # setting the words list.
    words_list = load_words_list()
    if len(words_list) == 0 or len(words_list) != runs_number:
        words_list = select_words(runs_number, agent.get_vocab())
        save_words_list(words_list)

    # setting the new smart trilateration algorithm
    setAgentAlgo(Alg.MultiLaterationAgent2.SmartMultiLateration, agent)

    if isinstance(agent.algorithm, MultiLaterationAgent2.SmartMultiLateration):
        agent.algorithm.set_error_method(error_method)
        agent.algorithm.set_vector_calculation_method(error_size_method)

    # init the statistics result for the algorithm
    calculator = Calculator()

    # iterate over each word and run the game
    for word in words_list:
        # results = OrderedDict()

        # setting the secret word in each session.
        agent.set_secret_word(word)
        agent.start_play(lambda args: args)

        # after run finished, collect the data.
        statistic = agent.get_statistics()

        # get the last guess and remaining words after it
        last_guess = max(statistic.keys())
        # remaining_words = statistic[last_guess]
        # add the result to the calculator
        calculator.add_error_result(last_guess)

        # reset the agent's data
        agent.reset_data()
    # After the data setting, Creating average of the results in calculator.
    Reporter.generate_error_graph(calculator.results, runs_number, words_list, model1_name, model2_name,
                                  error_method, error_size_method, error)
    agent.data.is_priority = False


def setAgentAlgo(algo_type, agent: Agent):
    if algo_type is Alg.MultiLateration.MultiLateration:
        agent.set_agent_MultiLateration_algorithm()
    elif algo_type is Alg.Naive.Naive:
        agent.set_agent_naive_algorithm()
    elif algo_type is Alg.NLateration.Trilateration:
        agent.set_agent_trilateration_algorithm()


def reload_graph_from_path(path):  # add another function from menu
    Reporter.generate_algo_guesses_from_csv(path)


def show_png_file(file_path):
    # Load the CSV file into a Pandas DataFrame
    img = plt.imread(file_path)
    plt.imshow(img)
    plt.show()


# =======================================Game Manager Class===============================================

class GameManager():
    def __init__(self):
        self.games = []
        self.statistics = []

    def add_game(self, agent, runs_number, game_type, algo_list, dist_name, host_model, agent_model, error,
                 error_method, size_method):
        game = {"agent": agent, "runs_number": runs_number, "game_type": game_type, "algo_list": algo_list,
                "dist_name": dist_name, "host_model": host_model, "agent_model": agent_model,"error":error,
                "error_method": error_method, "size_method": size_method}
        self.games.append(game)

    def run_games(self):
        for game in self.games:
            match game["game_type"]:  # The game type
                case "calculate_graph":
                    calculate_graph(game["runs_number"], game["agent"])  # number of runs and agent
                    continue
                case "calculate_algorithm_graph":
                    calculate_algorithm_graph(game["runs_number"], game["agent"],
                                              game["algo_list"])  # input algos dict? keep a global constant instead?
                    continue
                case "calculate_noise_to_guesses_graph":
                    calculate_noise_to_guesses_graph(game["runs_number"], game["agent"],
                                                     game["algo_list"], game["dist_name"], withQueue=False)  # input the rest?
                    continue
                case "create_error_compare_graph":
                    create_error_compare_graph(game["runs_number"], game["agent"], game["host_model"],
                                               game["agent_model"], game["error"], game["error_method"],
                                               game["size_method"])  # add methods to agent and name field
                    continue
                case _:
                    for i in range(game[0]):
                        game[1].start_play()
                        self.statistics.append(game[1].get_statistics())
                        # decide what to do with statistic or drop them instead
