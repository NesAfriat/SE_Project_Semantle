from abc import ABC, abstractmethod

from Business.Algorithms.BruteForce import BruteForce
from Business.Algorithms.Naive import Naive


class Agent(ABC):
    def __init__(self):
        self.model = None
        self.algorithm = None
        self.host = None
        self.last_score = None
        self.remain_words = None
        self.num_og_guesses = 0
        self.init_algo_data = lambda: None

    @abstractmethod
    def guess_word(self, data=None):
        pass

    def set_remain_words(self, remain_words):
        self.remain_words = remain_words

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def set_model(self, model):
        self.model = model
        self.remain_words = set(model.get_vocab())

    def set_host(self, host):
        self.host = host

    def set_init_algo_data(self, x):
        self.init_algo_data = x

    # only guess word should be abstract.
    def start_play(self, out):
        self.last_score = 0
        data = self.init_algo_data()
        while self.last_score != 1:
            word = self.guess_word(data)
            self.last_score = self.host.check_word(word)
            if self.last_score < 1:
                out("similarity is:" + str(self.last_score))
        out("you won!!")

    def inc_num_of_guesses(self):
        self.num_og_guesses = self.num_og_guesses + 1
