import random
import os.path
from pathlib import Path
import copy

import Business.ModelFactory as MF
from Business.Agents.Agent1 import Agent1
from Business.Agents.Agent2 import Agent2
from Business.Algorithms.BruteForce import BruteForce
from Business.Algorithms.Naive import Naive
from Business.Hosts.OfflineHost import OfflineHost

# from Business.Hosts.OnlineHost import OnlineHost
from Business.Hosts.OnlineHost import OnlineHost


class GameManager:
    WORD2VEC = "Google_Word2Vec.bin"

    def __init__(self):
        self.vocabulary = None
        self.trained = None
        self.host = None
        self.agent = None
        self.agent_model = None
        self.host_model = None

    def create_offline_host(self):
        self.host = OfflineHost()

    def create_online_host(self):
        self.host = OnlineHost()

    def set_host_word2vec_model(self):
        self.host_model,vocab = MF.load_from_file(self.WORD2VEC)
        self.host.set_model(self.host_model,vocab)

    def create_agent_word2vec_model(self):
        self.agent_model,vocab = MF.load_from_file(self.WORD2VEC)
        self.agent.set_model(self.agent_model, vocab)

    def set_agent_host_model(self):
        self.agent_model = copy.deepcopy(self.host_model)
        self.agent.set_model(self.agent_model)

    def set_gent_model(self):
        self.agent.set_model(self.agent_model)

    def create_agent1(self):
        self.agent = Agent1()
        self.agent.set_host(self.host)

    def create_agent2(self):
        self.agent = Agent2()
        self.agent.set_host(self.host)

    def setup_agent_model(self, model):
        self.agent = Agent2()
        self.agent.set_host(self.host)
        self.agent.set_model(model)

    def set_agent_Brute_Force_algorithm(self):
        algo = BruteForce(lambda words: (self.agent.set_remain_words(words)), self.agent.remain_words,
                          lambda w1, w2: self.agent_model.get_distance_of_word(w1, w2))
        self.agent.set_algorithm(algo)

    def set_agent_naive_algorithm(self):
        x = lambda dic: (self.agent.set_remain_words(dic), self.agent.inc_num_of_guesses())
        algo = Naive(x, self.agent.model.get_vocab())
        self.agent.set_algorithm(algo)

    def select_word(self):
        self.host.select_word_and_start_game()

    def start_human_game(self, inp, out):
        self.host.select_word_and_start_game(out)
        out("==================================================\nTry to Guess a word!")
        score = -1
        quit = False
        while score != 100 and not quit:
            word = inp("Enter your next word or 0 to return:\n")
            if word != '0':
                score = self.host.check_word(word)
                out("similarity is: \n" + str(round(score*100, 2)))
            else:
                quit = True
        if not quit:
            out("you won!!")
        else:
            out("see you next time!!")
        self.host.quitGame()

    def start_agent_game(self, out):
        self.host.select_word_and_start_game(out)
        self.agent.start_play(out)
