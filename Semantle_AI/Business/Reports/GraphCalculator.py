from collections import OrderedDict
import Business.Reports.ReportsGenerator as Reporter
import Business.Algorithms as Alg
from Business import MethodDistances
from Business.Agents.Agent import Agent
from Business.Algorithms import MultiLaterationAgent2
from Business.Reports.Calculator import Calculator
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
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), WORDS_LIST)
    try:
        with open(path, 'r') as file:
            lines = [line.strip() for line in file]
        return lines
    except FileNotFoundError:
        print(f"Error: {path} does not exist.")
        return []


def save_words_list(words_list):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), WORDS_LIST)
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


def calculate_algorithm_graph(runs_number, agent: Agent, algos_list: dict):
    # select the 'runs_number' words that will be run on each algorithm.
    words_list = select_words(runs_number, agent.get_vocab())

    # init the result
    # for each algo, run all words.
    for algo_name, algorithm in algos_list.items():

        setAgentAlgo(type(algorithm), agent)

        # initialize the statistics result for the algorithm
        calculator = Calculator()

        # iterate over each word and run the game
        for word in words_list:
            results = OrderedDict()

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
    for algo_name, algorithm in algos_list.items():
        # get the algo class
        setAgentAlgo(type(algorithm), agent)

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


def create_error_compare_graph(runs_number, agent: Agent, model1_name, model2_name):

    # setting the statistics to be by the priority heap and not remain words.
    agent.data.is_priority = True
    error = 1.00
    agent.data.setError(error)
    # setting the words list.
    words_list = load_words_list()
    if len(words_list) == 0 or len(words_list) != runs_number:
        words_list = select_words(runs_number, agent.get_vocab())
        save_words_list(words_list)

    # setting the new smart trilateration algorithm
    setAgentAlgo(Alg.MultiLaterationAgent2.SmartMultiLateration, agent)

    # setting the error vector methods values
    error_method = MultiLaterationAgent2.SUM
    error_size_method = MultiLaterationAgent2.NORM1

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


def reload_graph_from_path(path):
    Reporter.generate_algo_guesses_from_csv(path)


def show_png_file(file_path):
    # Load the CSV file into a Pandas DataFrame
    img = plt.imread(file_path)
    plt.imshow(img)
    plt.show()
