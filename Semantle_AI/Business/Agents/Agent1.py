from abc import abstractmethod, ABC

from Business.Agents.Agent import Agent
import random


class Agent1(Agent):
    def __init__(self):
        super().__init__()

    def guess_word(self, *args):
        self.last_word = self.algorithm.calculate(*args)
        return self.last_word
    def set_host_model(self):
        self.set_model(self.host.model)
