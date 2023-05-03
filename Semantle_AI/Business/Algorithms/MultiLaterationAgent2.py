import random
from Semantle_AI.Business.Agents.Data import MyItem, GuessScore
from Semantle_AI.Business.Algorithms.Algorithm import Algorithm
import torch
import numpy as np

SUM = "SUM"
SUM_RELATIVE = "Sum_Relative"
BRUTE_FORCE = "Brute_force"
NORM2 = "Norm2"
NORM1 = "Norm1"


class SmartMultiLateration(Algorithm):
    def __init__(self, dist_formula, vec_calc_method=SUM, vec_value_method=NORM2):
        super().__init__()
        self.dist_formula = dist_formula
        self.error_calculation_forms = dict([(SUM, self.sum), (SUM_RELATIVE, self.sum_relative),
                                             (BRUTE_FORCE, self.ret_zero)])
        self.vector_value_forms = dict([(NORM2, self.mse), (NORM1, self.sum_vec)])
        self.error_calc_method = vec_calc_method
        self.vector_value_method = vec_value_method
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def set_error_method(self, method_name):
        self.error_calc_method = method_name

    def set_vector_calculation_method(self, method_name):
        self.vector_value_method = method_name

    @staticmethod
    def in_range(distance1, distance2, percentage_error):
        percentage_difference = abs((distance1 - distance2) / distance2) * 100
        return percentage_difference <= percentage_error

    def sum_relative(self, word):
        last_guess: GuessScore = self.data.scores[-1]
        dist_from_secret = last_guess.score
        dist_from_guess = self.data.model.get_distance_of_word(last_guess.word, word)
        return (dist_from_secret - dist_from_guess) / dist_from_secret

    def sum(self, word):
        last_guess: GuessScore = self.data.scores[-1]
        dist_from_secret = last_guess.score
        dist_from_guess = self.data.model.get_distance_of_word(last_guess.word, word)
        return dist_from_secret - dist_from_guess

    @staticmethod
    def mse(vector):
        tensor = torch.tensor(vector)
        mse = float(torch.mean((tensor ** 2).float()))
        return torch.sqrt(torch.tensor(mse))

    def sum_vec(self, vector):
        new_vec = [abs(x) for x in vector]
        tensor_vector = torch.tensor(new_vec, dtype=torch.float32, device=self.device)
        return torch.sum(tensor_vector).item()

    @staticmethod
    def norm_i(i, weight, val):
        val = torch.pow(torch.tensor(abs(val)), i).item()
        return weight + val

    @staticmethod
    def ret_zero(word):
        return 0

    def calculate_new_error_val(self, word):
        if self.error_calc_method == SUM:
            return self.sum(word)
        elif self.error_calc_method == SUM_RELATIVE:
            return self.sum_relative(word)
        elif self.error_calc_method == BRUTE_FORCE:
            return self.ret_zero(word)

    def calculate_new_weight(self, weight, val):
        if self.vector_value_method == NORM2:
            return self.norm_i(2, weight, val)
        elif self.vector_value_method == NORM1:
            return self.norm_i(1, weight, val)

    def calculate(self):

        # Modify the items in the queue
        for item in self.data.words_heap:
            # calc new val to add the vector.
            val = self.calculate_new_error_val(item.word)

            # updating the error vector in the queue, and update the weight.
            item.error_vec.append(val)
            item.weight = self.calculate_new_weight(item.weight, val)

        # sanity check
        if len(self.data.words_heap) == 0:
            raise ValueError("error occurred, there are no words left to guess.")
        # return the queue top.
        if self.error_calc_method != BRUTE_FORCE:
            next_word = self.data.words_heap[0]
            self.data.words_heap.remove(next_word)
        else:
            next_word = random.choice(self.data.words_heap)
            self.data.words_heap.remove(next_word)
        return next_word.word
