from Business.Algorithms.Algorithm import Algorithm
import pandas as pd
import random


class Naive(Algorithm):
    def __init__(self, on_guess, vocab):
        super().__init__(on_guess)
        self.vocab = vocab

    def calculate(self, *args):
        el = random.sample(self.vocab, 1)[0]
        self.vocab.remove(el)
        self.on_guess(self.vocab)
        return el
