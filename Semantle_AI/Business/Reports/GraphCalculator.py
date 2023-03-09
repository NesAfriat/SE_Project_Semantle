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
        calculator = Calculator(runs_number)
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
    right_guesses = OrderedDict()
    # init the result
    # for each algo, run all words.
    counter = 0
    for algo_name in algos_list:
        counter = counter + 1
        # get the algo class
        algorithm = algos_list[algo_name]
        if type(algorithm) is alg.MultiLateration.MultiLateration:
            agent.set_agent_MultiLateration_algorithm()
        elif type(algorithm) is alg.Naive.Naive:
            agent.set_agent_naive_algorithm()
        elif type(algorithm) is alg.NLateration.Trilateration:
            agent.set_agent_trilateration_algorithm()
        # init the statistics result for the algorithm
        calculator = Calculator(runs_number)
        # iterate over each word and run the game
        for word in words_list:
            results = OrderedDict()
            # setting the secret word in each session.
            agent.set_secret_word(word)
            agent.start_play(lambda args: args)
            # after run finished, collect the data.
            statistics = agent.get_statistics()
            for key in statistics.keys():
                results[key] = statistics[key]
            agent.reset_data()
            max_val = calculator.get_highest_nonzero_key(results)
            calculator.add_result(max_val, results[max_val])
            # After creating average
        reporter.generate_graph(calculator.results.keys(), algo_name, runs_number)


def reload_graph_from_path(path):
    reporter.generate_algo_guesses_from_csv(path)

def show_png_file(file_path):
    # Load the CSV file into a Pandas DataFrame
    img = plt.imread(file_path)
    plt.imshow(img)
    plt.show()
