from abc import ABC, abstractmethod

from Semantle_AI.Business.Algorithms.Naive import Naive


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

    @abstractmethod
    def start_play(self, inp, out):
        out("==================================================\nTry to Guess a word,\npress 0 to exit: ")
        score = -1
        while score != 1:
            word = inp("-please guess a word: \n")
            score = self.host.check_word(word)
            if score < 1:
                out("similarity is:" + str(score))
        out("you won!!")
