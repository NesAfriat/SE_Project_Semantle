from abc import ABC, abstractmethod
import random

from Business.Algorithms.Algorithm import Algorithm


class BruteForce(Algorithm):
    def __init__(self, dist_formula):
        super().__init__()
        self.dist_formula = dist_formula

    def calculate(self, *args):
        v = self.data.get_word_vec(self.data.last_word)
        self.data.remain_words = [x for x in
                                  filter(lambda x: abs(self.dist_formula(self.data.get_word_vec(x), v) - self.data.last_score) <= 0.0001,
                                         self.data.remain_words)]
        if len(self.data.remain_words) == 0:
            raise ValueError("error occurred, there are no words left to guess.")
        return random.choice(self.data.remain_words)
