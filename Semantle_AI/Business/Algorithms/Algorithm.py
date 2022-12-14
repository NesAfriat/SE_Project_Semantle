from abc import ABC, abstractmethod


class Algorithm(ABC):
    def __init__(self, on_guess):
        self.on_guess = on_guess
        pass

    @abstractmethod
    def calculate(self,data = None):
        pass
