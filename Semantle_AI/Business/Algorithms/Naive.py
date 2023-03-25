from Business.Algorithms.Algorithm import Algorithm
import random


class Naive(Algorithm):
    def __init__(self):
        super().__init__()

    def calculate(self):
        words = self.data.remain_words
        el = random.sample(words, 1)[0]
        words.remove(el)
        self.data.remain_words = words
        return el
