from abc import abstractmethod

from Semantle_AI.Business.Agents.Agent import Agent
from Semantle_AI.Business.Algorithms.Naive import Naive


class Agent2(Agent):

    def __init__(self):
        super().__init__()

    def guess_word(self):
        pass