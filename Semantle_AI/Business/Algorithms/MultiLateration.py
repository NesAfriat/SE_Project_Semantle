from abc import ABC, abstractmethod
import random

from Business.Algorithms.Algorithm import Algorithm


class MultiLateration(Algorithm):
    def __init__(self, dist_formula):
        super().__init__()
        self.dist_formula = dist_formula

    def calculate(self):
        def in_error_range(distance1, distance2, percentage_error):
            """
            Returns True if the percentage difference between distance1 and distance2 is within percentage_error, False otherwise.
            """
            percentage_difference = abs((distance1 - distance2) / distance2) * 100
            return percentage_difference <= percentage_error

        last_vec = self.data.get_word_vec(self.data.last_word)

        self.data.remain_words = [x for x in
                                  filter(lambda x: in_error_range(
                                      self.dist_formula(self.data.get_word_vec(x), last_vec),
                                      self.data.last_score,
                                      self.data.error),
                                         self.data.remain_words)]
        if len(self.data.remain_words) == 0:
            raise ValueError("error occurred, there are no words left to guess.")
        return random.choice(self.data.remain_words)


