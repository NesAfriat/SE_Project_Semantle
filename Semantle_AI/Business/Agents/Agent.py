from abc import ABC, abstractmethod

from Business.Algorithms.Naive import Naive


class Agent(ABC):
    def __init__(self, algorithm=Naive()):
        self.model = None
        self.algorithm = algorithm
        self.host = None

    @abstractmethod
    def guess_word(self):
        pass

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def set_model(self, model):
        self.model = model

    def set_host(self, host):
        self.host = host

    # only guess word should be abstract.
    def start_play(self, out):
        score = -1
        while score != 1:
            word = self.guess_word()
            score = self.host.check_word(word)
            if score < 1:
                out("similarity is:" + str(score))
        out("you won!!")
