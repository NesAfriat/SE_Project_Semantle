from abc import abstractmethod, ABC

from Semantle_AI.Business.Agents.Agent import Agent
from Semantle_AI.Business.Algorithms.Naive import Naive


class Agent1(Agent):
    def guess_word(self):
        pass

    def __init__(self):
        super().__init__()
