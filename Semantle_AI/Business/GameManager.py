import random
import os.path
from pathlib import Path

import Business.ModerFactory as MF
from Business.Agents.Agent1 import Agent1
from Business.Agents.Agent2 import Agent2
from Business.Algorithms.BruteForce import BruteForce
from Business.Algorithms.Naive import Naive
from Business.Hosts.OfflineHost import OfflineHost

# from Business.Hosts.OnlineHost import OnlineHost
from Business.Hosts.OnlineHost import OnlineHost


class GameManager:
    WORD2VEC = "word2vec.wordvectors"

    def __init__(self):
        self.vocabulary = None
        self.trained = None
        self.host = None
        self.agent = None

    def create_offline_host(self):
        self.host = OfflineHost()

    def create_online_host(self):
        self.host = OnlineHost()

    def set_host_word2vec_model(self):
        model = MF.load_from_file(self.WORD2VEC)
        self.host.set_model(model)

    def set_gent_word2vec_model(self):
        model = MF.load_from_file(self.WORD2VEC)
        self.agent.set_model(model)

    def delete_host(self):
        self.host = None

    def create_glove_model(self):
        pass

    def create_agent1(self):
        self.agent = Agent1()
        self.agent.set_host(self.host)
        self.agent.set_model(self.host.get_model())

    def create_agent2(self):
        self.agent = Agent2()
        self.agent.set_host(self.host)

    def setup_agent_model(self, model):
        self.agent = Agent2()
        self.agent.set_host(self.host)
        self.agent.set_model(model)

    def set_agent_Brute_Force_algorithm(self):
        def help(dict):
            self.agent.inc_num_of_guesses()
            new_dict = dict & self.agent.remain_words
            self.agent.set_remain_words(dict & self.agent.remain_words)
            return new_dict
        init_data = lambda x: self.host.guess_word()
        self.agent.set_init_algo_data(init_data)


        x = lambda dic: (self.agent.inc_num_of_guesses(), help)
        algo = BruteForce(x, self.agent.model.get_vocab(), lambda w1, w2: self.agent.model.get_distance_of_word(w1, w2))

        set_data_on_guess = lambda dist: algo.set_dist(dist)

        self.agent.set_algorithm(algo)

    def set_agent_naive_algorithm(self):
        x = lambda dic: (self.agent.set_remain_words(dic), self.agent.inc_num_of_guesses())
        algo = Naive(x, self.agent.model.get_vocab())
        self.agent.set_algorithm(algo)

    def select_word(self):
        self.host.select_word_and_start_game()

    def start_human_game(self, inp, out):
        self.host.select_word_and_start_game()
        out("==================================================\nTry to Guess a word,\npress 0 to exit: ")
        score = -1
        while score != 1:
            word = inp("please guess a word: \n")
            score = self.host.check_word(word)
            if score < 1:
                out("similarity is: \n" + str(score))
        self.host.quit()
        out("you won!!")

    def start_agent_game(self, out):
        self.host.select_word_and_start_game()
        self.agent.start_play(out)
