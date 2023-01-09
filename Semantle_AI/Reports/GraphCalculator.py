import copy
import Reports.ReportsGenerator as reporter
import Business.Model
import random
import Business.Algorithms as alg
from Business import MethodDistances
from Business.Agents.Agent import Agent
from Business.Model.Model import Model
from Reports.Calculator import Calculator

WORD2VEC = "Google_Word2Vec.bin"
DISTANCE_METHOD = "Euclid"


def select_words(num_of_words, vocab):
    ret = set()
    while len(ret) < num_of_words:
        to_add = vocab.pop()
        if to_add not in ret:
            ret.add(to_add)
    return ret


def calculate_graph(runs_number, agent: Agent):
    # select the 'runs_number' words that will be run on each algorithm.
    words_list = select_words(runs_number, agent.get_vocab())
    algo_dict = dict({"Brute_force": alg.Naive.Naive(),
                      "Multi-Lateration ": alg.BruteForce.BruteForce(MethodDistances.euclid_function()),
                      "Trilateration": alg.Trilateration.Trilateration()})
    vocabulary = copy.copy(agent.get_vocab())
    # init the result
    # for each algo, run all words.
    counter = 0
    for algo_name in algo_dict:
        counter = counter + 1
        # get the algo class
        algorithm = algo_dict[algo_name]
        if type(algorithm) is alg.BruteForce.BruteForce:
            agent.set_agent_Brute_Force_algorithm()
        elif type(algorithm) is alg.Naive.Naive:
            agent.set_agent_naive_algorithm()
        elif type(algorithm) is alg.Trilateration.Trilateration:
            agent.set_agent_trilateration_algorithm()
        # init the statistics result for the algorithm
        calculator = Calculator(runs_number)
        # iterate over each word and run the game
        for word in words_list:
            # setting the secret word in each session.
            agent.set_secret_word(word)
            #agent.reset_data()
            agent.start_play(lambda args: args)
            # after run finished, collect the data.
            statistics = agent.get_statistics()
            for key in statistics.keys():
                calculator.add_result(key, statistics[key])
            agent.reset_data()
            # After creating average
        k = calculator.calc()
        for key in k.keys():
            res = k[key]
            if key == list(k.keys())[-1]:
                reporter.save_guess_data(counter, key, 0)
            else:
                reporter.save_guess_data(counter, key, res)

        reporter.save_game_data(counter, WORD2VEC, WORD2VEC, algo_name, DISTANCE_METHOD)
    print(len(reporter.game_guesses))
    print(len(reporter.games_data))
    reporter.generate_algo_guesses_from_csv()



