from abc import ABC, abstractmethod
import random
from Business.Algorithms.Algorithm import Algorithm


class BruteForce(Algorithm):
    def __init__(self, on_guess, dict, dis_calculate):
        super().__init__(on_guess)
        self.dict = set(dict)
        self.dis_calculate = dis_calculate
        self.distance = None

    def calculate(self):
        pass

    def set_dist(self,distance):
        self.distance = distance
