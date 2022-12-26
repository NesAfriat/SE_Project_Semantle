from Business.Algorithms.Algorithm import Algorithm
import pandas as pd
import random


class Naive(Algorithm):
    def __init__(self, on_guess, vocab):
        super().__init__(on_guess)
        self.vocab = vocab

    def calculate(self, *args):
        w = random.choice(self.vocab)
        self.vocab.remove(w)
        self.on_guess(self.vocab)
        return w
