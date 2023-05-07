import random

import numpy as np

from Semantle_AI.Business.Agents.Data import GuessScore
from Semantle_AI.Business.Algorithms.Algorithm import Algorithm
import torch

SUM = "SUM"
SUM_RELATIVE = "Sum_Relative"
BRUTE_FORCE = "Brute_force"
NORM2 = "Norm2"
NORM1 = "Norm1"
PROB = "Relative_Probability"

VOI = "VOIS"

class SmartMultiLateration(Algorithm):
    def __init__(self, dist_formula, vec_calc_method=SUM, vec_value_method=NORM2):
        super().__init__()
        self.dist_formula = dist_formula
        self.error_calculation_forms = dict([(SUM, self.sum), (SUM_RELATIVE, self.sum_relative),
                                             (BRUTE_FORCE, self.ret_zero)])
        self.vector_value_forms = dict([(NORM2, self.mse), (NORM1, self.sum_vec), (PROB, self.prob), (VOI, self.voi)])
        self.error_calc_method = vec_calc_method
        self.vector_value_method = vec_value_method
        self.finish_calc_needed = not(self.vector_value_method == NORM1 or self.vector_value_method == NORM2)
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


    def modified_euclidean_distance(self, vector):
        # calculating the vector of eulid.
        e_vector_array = np.array(vector)
        squared_e_vector = np.square(e_vector_array)
        sum_squared_e_vector = np.sum(squared_e_vector)
        cardinality = len(vector)
        e_w_s = (1 / cardinality) * np.sqrt(sum_squared_e_vector)
        return e_w_s


    def f_w_s(self, vector):
        return np.exp(self.modified_euclidean_distance(vector))

    def norm_factor(self, e, vectors):
        sum_f_w_s = 0
        for vector in vectors:
            e_w_s = self.modified_euclidean_distance(vector)
            f_w_s_value = self.f_w_s(e_w_s)
            sum_f_w_s += f_w_s_value
        return sum_f_w_s

    @staticmethod
    def p_w_s(f_w_s_value, norm_factor_value):
        return f_w_s_value / norm_factor_value

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

    def calculate_new_weight(self, vector, weight, val):
        if self.vector_value_method == NORM2:
            return self.norm_i(2, weight, val)
        elif self.vector_value_method == NORM1:
            return self.norm_i(1, weight, val)

    def prob(self, items, norm_form):
        for item in items:
            # remove the current item from the sorted list
            self.data.words_heap.remove(item)
            item.weight = item.weight / norm_form

            # insert the item back into the sorted list with its new weight
            self.data.words_heap.add(item)

    def voi(self, items, norm_form):

        E_s = 0
        E_s_w = 0
        for item in items:
            E_s -= item.weight*np.log2(item.weight)
            # todo: NEEDED TO COMPLETE.


    def calculate_rest(self):


    def handle_calculation(self, item, norm_form, val):

        # checking the calculation method.
        if not self.finish_calc_needed:
            # remove the current item from the sorted list
            self.data.words_heap.remove(item)

            # update the weight of the item
            new_weight = self.calculate_new_weight(item.error_vec, item.weight, val)
            item.weight = new_weight

            # insert the item back into the sorted list with its new weight
            self.data.words_heap.add(item)
        else:
            # remove the current item from the sorted list
            self.data.words_heap.remove(item)

            # update the weight of the item
            f_w_s = self.f_w_s(item.error_vec)
            norm_form += f_w_s
            item.weight = f_w_s

    def finish_calculation(self, items, norm_form):
        # if need to continue calculation.
        if self.finish_calc_needed:
            if self.vector_value_method == PROB:
                self.prob( items, norm_form)
            elif self.vector_value_method == VOI:
                self.prob(items, norm_form)
                self.voi( items, norm_form)

    def choose_next(self, items):
        # sanity check
        if len(items) == 0:
            raise ValueError("error occurred, there are no words left to guess.")
        # return the queue top.
        if self.error_calc_method != BRUTE_FORCE:
            next_word = items.pop(0)
        else:
            next_word = random.choice(items)
            items.remove(next_word)
        return next_word.word

    def calculate(self):

        norm_form = 0

        # Modify the items in the queue
        for item in self.data.words_heap:

            # calc new val to add the vector.
            val = self.calculate_new_error_val(item.word)

            # updating the error vector in the queue, and update the weight.
            item.error_vec.append(val)

            self.handle_calculation(item, norm_form, val)

            self.finish_calculation(self.data.words_heap, norm_form)

        return self.choose_next(self.data.words_heap)



