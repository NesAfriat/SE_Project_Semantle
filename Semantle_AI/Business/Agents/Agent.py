
from abc import ABC, abstractmethod

from Semantle_AI.Business.Algorithms.Naive import Naive


class Agent(ABC):
    def __init__(self, algorithm=Naive()):
        self.model = None
        self.algorithm = algorithm

    @abstractmethod
    def guess_word(self):
        pass

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def set_model(self, model):
        self.model = model
