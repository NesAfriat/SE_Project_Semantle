import copy
from collections import OrderedDict

import Business.Reports.ReportsGenerator as reporter
import Business.Algorithms as alg
from Business import MethodDistances
from Business.Agents.Agent import Agent
from Business.Reports.Calculator import Calculator
import tkinter as tk
import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt

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
                      "Multi-Lateration ": alg.MultiLateration.MultiLateration(MethodDistances.euclid_function()),
                      "Trilateration": alg.NLateration.Trilateration()})

    # init the result
    # for each algo, run all words.
    counter = 0
    for algo_name in algo_dict:
        counter = counter + 1
        # get the algo class
        algorithm = algo_dict[algo_name]
        if type(algorithm) is alg.MultiLateration.MultiLateration:
            agent.set_agent_MultiLateration_algorithm()
        elif type(algorithm) is alg.Naive.Naive:
            agent.set_agent_naive_algorithm()
        elif type(algorithm) is alg.NLateration.Trilateration:
            agent.set_agent_trilateration_algorithm()
        # init the statistics result for the algorithm
        calculator = Calculator()
        # iterate over each word and run the game
        for word in words_list:
            # setting the secret word in each session.
            agent.set_secret_word(word)
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
    path = reporter.generate_data_files()
    reporter.generate_algo_guesses_from_csv(path)


def calculate_algorithm_graph(runs_number, agent: Agent, algos_list):
    # select the 'runs_number' words that will be run on each algorithm.
    words_list = select_words(runs_number, agent.get_vocab())
    # init the result
    # for each algo, run all words.
    for algo_name in algos_list:
        # get the algo class
        algorithm = algos_list[algo_name]
        setAgentAlgo(type(algorithm), agent)
        # init the statistics result for the algorithm
        calculator = Calculator()
        # iterate over each word and run the game
        for word in words_list:
            results = OrderedDict()

            # setting the secret word in each session.
            agent.set_secret_word(word)
            agent.start_play(lambda args: args)

            # after run finished, collect the data.
            statistics = agent.get_statistics()

            # insert in result the data from statistic by order(by guess num)
            for key in statistics.keys():
                results[key] = statistics[key]

            # set up for next iteration. reset data in agent.
            agent.reset_data()

            # taking the last guess and to remain words after it.
            max_val = calculator.get_highest_nonzero_key(results)

            # calculating the graph values to be the number of guesses needed to win.
            calculator.add_result(max_val, results[max_val])

        # After the data setting, Creating average of the results in calculator.
        reporter.generate_graph(calculator.results.keys(), algo_name, runs_number)


def calculate_noise_to_guesses_graph(runs_number, agent: Agent, algos_list):
    # select the noises for each run.
    noises_list = [1.0, 1.005, 1.01, 1.02, 1.05, 1.1, 1.15, 1.2, 1.5]

    # select the 'runs_number' words that will be run on each algorithm.
    words_list = select_words(runs_number, agent.get_vocab())

    # for each algo, run all words, and in different noises acceptance.
    for algo_name in algos_list:
        # get the algo class
        algorithm = algos_list[algo_name]
        setAgentAlgo(type(algorithm), agent)
        # init the statistics result for the algorithm
        calculator = Calculator()
        # run each word with each noise
        for noise in noises_list:
            # setting the runs current error.
            agent.data.set_error(noise)
            # iterate over each word and run the game
            for word in words_list:
                results = OrderedDict()

                # setting the secret word in each session.
                agent.set_secret_word(word)
                agent.start_play(lambda args: args)

                # after run finished, collect the data.
                statistics = agent.get_statistics()

                # insert in result the data from statistic by order(by guess num)
                for key in statistics.keys():
                    results[key] = statistics[key]

                # set up for next iteration. reset data in agent.
                agent.reset_data()

                # taking the last guess and to remain words after it.
                max_val = calculator.get_highest_nonzero_key(results)

                # calculating the graph values to be the number of guesses needed to win.
                calculator.add_result(noise, max_val)

        # After the data setting, Creating average of the results in calculator.
        reporter.generate_noises_graph(calculator.results, algo_name, runs_number)


def setAgentAlgo(algo_type, agent: Agent):
    if algo_type is alg.MultiLateration.MultiLateration:
        agent.set_agent_MultiLateration_algorithm()
    elif algo_type is alg.Naive.Naive:
        agent.set_agent_naive_algorithm()
    elif algo_type is alg.NLateration.Trilateration:
        agent.set_agent_trilateration_algorithm()


def reload_graph_from_path(path):
    reporter.generate_algo_guesses_from_csv(path)


def show_png_file(file_path):
    # Load the CSV file into a Pandas DataFrame
    img = plt.imread(file_path)
    plt.imshow(img)
    plt.show()
