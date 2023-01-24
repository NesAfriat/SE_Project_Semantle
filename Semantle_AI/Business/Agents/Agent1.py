from abc import abstractmethod, ABC

from Business.Agents.Agent import Agent
import random


class Agent1(Agent):
    def __init__(self):
        super().__init__()
        self.last_word = None

    def guess_word(self):
        self.last_word = self.algorithm.calculate()
        return self.last_word

    def set_host_model(self):
        self.set_model(self.host.model)



