from abc import abstractmethod

from Semantle_AI.Business.Algorithms.Naive import Naive


class Agent1:
    def __init__(self, model, algorithm=Naive()):
        self.model = model
        self.algorithm = algorithm

    def guess_word(self):
        pass

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

