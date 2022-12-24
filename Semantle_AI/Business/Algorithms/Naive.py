
from Business.Algorithms.Algorithm import Algorithm
import pandas as pd


class Naive(Algorithm):
    def __init__(self, on_guess, vocab: set):
        super().__init__(on_guess)
        self.vocab = vocab
        data = pd.read_csv(r'Vocab/unigram_freq.csv')
        df = pd.DataFrame(data, columns=['word', 'count'])
        print(len(df))
    def calculate(self,data = None):
        w = self.vocab.pop()
        self.on_guess(self.vocab)
        return str.lower(w)
