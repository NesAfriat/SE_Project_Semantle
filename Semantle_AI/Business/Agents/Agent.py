from abc import ABC, abstractmethod

from Business.Algorithms.Naive import Naive
from Business.Data import Data


def add_to_list(last_word):
    pass


class Agent(ABC):
    def __init__(self):
        self.algorithm = None
        self.host = None
        self.num_og_guesses = 0
        self.init_algo_data = lambda: None
        self.data = Data()
        self.end_score = None
        self.init = None

    @abstractmethod
    def guess_word(self, *args):
        pass

    def set_end_score(self, end_score):
        self.end_score = end_score

    def set_algorithm(self, algorithm, init_func):
        self.algorithm = algorithm
        self.algorithm.set_data(self.data)
        self.init = init_func

    def set_model(self, model):
        self.data.set_model(model)

    def set_host(self, host):
        self.host = host

    # only guess word should be abstract.
    def start_play(self, out):
        self.data.last_score = -1

        # for brute force
        self.init()
        while abs(self.data.last_score - self.end_score) > 0.0001:
            try:
                word = self.guess_word(self.data.last_word, self.data.last_score, self.data)

                self.data.last_score = self.host.check_word(word)
                self.data.last_word = word

                if self.data.last_score == -2:
                    add_to_list(self.data.last_word)
                    self.guess_random_word()
                out(f"similarity for the word  {self.data.last_word} is:  {str(round(self.data.last_score * 100, 2))}")
            except ValueError as e:
                out(e)
                return
        out("you won!!")

    def set_last_score(self, score):
        self.data.last_score = score

    def guess_random_word(self):
        guess = ""
        dist = -2
        algo = Naive()
        algo.set_data(self.data)
        while dist == -2:
            if self.data.last_word is not None:
                add_to_list(self.data.last_word)
            guess = algo.calculate()
            dist = self.host.check_word(guess)
        self.data.add_to_dict(guess, dist, self.data.model.get_word_vec(guess))

    def guess_n_random_word(self, n):
        for i in range(n):
            self.guess_random_word()

    def inc_num_of_guesses(self):
        self.num_og_guesses = self.num_og_guesses + 1
