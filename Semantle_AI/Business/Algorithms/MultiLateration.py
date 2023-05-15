from abc import ABC, abstractmethod
import random

from Semantle_AI.Business.Algorithms.Algorithm import Algorithm


def in_range(distance1, distance2, percentage_error):
    """
    Returns True if the percentage difference between distance1 and distance2 is within percentage_error, False otherwise.
    """
    percentage_difference = abs((distance1 - distance2) / distance2) * 100
    return percentage_difference <= percentage_error


class MultiLateration(Algorithm):
    def __init__(self, dist_formula):
        super().__init__()
        self.dist_formula = dist_formula

    def calculate(self):
        last_vec = self.data.get_word_vec(self.data.last_word)

        res = []
        for x in self.data.remain_words:
            if in_range(self.dist_formula(self.data.get_word_vec(x), last_vec), self.data.last_score, 0.01):
                res.append(x)

        self.data.remain_words = res
        if len(self.data.remain_words) == 0:
            raise ValueError("error occurred, there are no words left to guess.")
        return random.choice(self.data.remain_words)
