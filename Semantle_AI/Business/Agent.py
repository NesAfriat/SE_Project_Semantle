

from abc import ABC, abstractmethod


class Agent(ABC):
    def __init__(self, num_of_guess=0):
        pass

    @abstractmethod
    def guess_word(self):
        pass
