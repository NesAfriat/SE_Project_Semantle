import copy

import Business.Model
import random

import Business.Algorithms as alg
from Business import MethodDistances
from Business.Agents.Agent import Agent
from Business.Model.Model import Model


def select_words(num_of_words, vocab):
    ret = set()
    for i in range(0, num_of_words):
        ret.add(vocab.pop)
    return ret


def calculate_graph(runs_number, agent: Agent):
    # select the 'runs_number' words that will be run on each algorithm.
    words_list = select_words(runs_number, agent.get_vocab())
    algo_dict = dict({"Naive": alg.Naive.Naive(),
                      "Brute_force": alg.BruteForce.BruteForce(MethodDistances.euclid_function()),
                      "Trilateration": alg.Trilateration.Trilateration()})
    vocabulary = copy.copy(agent.get_vocab())
    # for each algo, run all words.
    for algo_name in algo_dict:
        # get the algo class
        algorithm = algo_dict[algo_name]
        if algorithm is alg.BruteForce.BruteForce:
            set_Brute_Force_algorithm(algorithm, agent)
        elif algorithm is alg.Naive.Naive:
            set_naive_algorithm(algorithm, agent)
        elif algorithm is alg.Trilateration.Trilateration:
            set_trilateration_algorithm(algorithm, agent)
        agent.set_algorithm(algorithm, agent)
        # iterate over each word and run the game
        for word in words_list:
            # setting the secret word in each session.
            agent.set_secret_word(word)
            agent.reset_data(vocabulary)
            agent.start_play(lambda *args: print(*args))
            # after run finished, collect the data.
            statistics = agent.get_statistics()

def set_Brute_Force_algorithm(algo: alg.BruteForce.BruteForce, agent: Agent):
    agent.set_algorithm(algo, lambda: agent.guess_n_random_word(1))


def set_naive_algorithm(algo: alg.Naive.Naive, agent: Agent):
    agent.set_algorithm(algo, lambda: None)


def set_trilateration_algorithm(algo: alg.Trilateration.Trilateration, agent: Agent):
    agent.set_algorithm(algo, lambda: agent.guess_n_random_word(agent.agent_model.get_number_of_dim() + 1))
