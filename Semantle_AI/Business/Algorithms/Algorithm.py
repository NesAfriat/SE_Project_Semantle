from abc import ABC, abstractmethod

from Business.Agents.Data import Data


class Algorithm(ABC):
    def __init__(self):
        self.data = None

    @abstractmethod
    def calculate(self):
        pass

    def set_data(self, data: Data):
        self.data = data
