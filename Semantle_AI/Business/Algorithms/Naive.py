from Business.Algorithms.Algorithm import Algorithm
import pandas as pd


class Naive(Algorithm):
    def __init__(self, on_guess, vocab: set):
        super().__init__(on_guess)
        self.vocab = vocab

    def calculate(self, *args):
        w = self.vocab.pop()
        self.on_guess(self.vocab)
        return w
