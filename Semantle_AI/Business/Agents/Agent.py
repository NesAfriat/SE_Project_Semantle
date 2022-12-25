from abc import ABC, abstractmethod

from Business.Algorithms.BruteForce import BruteForce
from Business.Algorithms.Naive import Naive


class Agent(ABC):
    def __init__(self):
        self.model = None
        self.algorithm = None
        self.host = None
        self.last_score = None
        self.last_word = None
        self.remain_words = None
        self.num_og_guesses = 0
        self.init_algo_data = lambda: None

    @abstractmethod
    def guess_word(self, *args):
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
        # for brute force
        self.guess_random_word()

        while self.last_score != 100:
            word = self.guess_word(self.last_word, self.last_score)
            self.last_score = self.host.check_word(word)
            out("similarity is:" + str(self.last_score))
        out("you won!!")

    def set_last_score(self, score):
        self.last_score = score

    def guess_random_word(self):
        guess = ""
        dist = -2
        alog = Naive(lambda x: self.set_remain_words(x), self.model.vocab)
        while dist == -2:
            guess = alog.calculate()
            dist = self.host.check_word(guess)
        self.last_word = guess
        self.last_score = dist

    def inc_num_of_guesses(self):
        self.num_og_guesses = self.num_og_guesses + 1
