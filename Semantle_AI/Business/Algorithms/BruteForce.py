from abc import ABC, abstractmethod
import random

from Business.Algorithms.Algorithm import Algorithm


class BruteForce(Algorithm):
    def __init__(self, on_guess, vocab: set, dist_formula):
        super().__init__(on_guess)
        self.vocab = vocab
        self.dist_formula = dist_formula

    def calculate(self, *args):
        dist = args[1]
        self.vocab = [x for x in filter(lambda x:  abs(self.dist_formula(x, args[0]) - dist) <= 0.01, self.vocab)]
        self.on_guess(self.vocab)
        if len(self.vocab) == 0:
            raise ValueError("error occurred, there are no words left to guess.")
        return random.choice(self.vocab)

    def set_dist(self, distance):
        self.distance = distance
