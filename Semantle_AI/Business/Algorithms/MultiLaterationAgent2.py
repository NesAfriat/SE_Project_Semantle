import functools
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
VOI = "VOI"


class SmartMultiLateration(Algorithm):
    def __init__(self, dist_formula, vec_calc_method=SUM, vec_value_method=NORM2):
        super().__init__()
        self.dist_formula = dist_formula
        self.error_calculation_forms = dict([(SUM, self.sum), (SUM_RELATIVE, self.sum_relative),
                                             (BRUTE_FORCE, self.ret_zero)])
        self.vector_value_forms = dict([(NORM2, self.mse), (NORM1, self.sum_vec), (PROB, self.prob), (VOI, self.voi)])
        self.error_calc_method = vec_calc_method
        self.vector_value_method = vec_value_method
        self.using_entropy = not (self.vector_value_method == NORM1 or self.vector_value_method == NORM2)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def set_error_method(self, method_name):
        self.error_calc_method = method_name
        self.using_entropy = not (self.vector_value_method == NORM1 or self.vector_value_method == NORM2)

    def set_vector_calculation_method(self, method_name):
        self.vector_value_method = method_name
        self.using_entropy = not (self.vector_value_method == NORM1 or self.vector_value_method == NORM2)

    @staticmethod
    def in_range(distance1, distance2, percentage_error):
        percentage_difference = abs((distance1 - distance2) / distance2) * 100
        return percentage_difference <= percentage_error

    def sum_relative(self, word):
        last_guess: GuessScore = self.data.scores[-1]
        dist_from_secret = last_guess.score
        dist_from_guess = self.data.get_distance_of_word(last_guess.word, word)
        return (dist_from_secret - dist_from_guess) / dist_from_secret

    def sum(self, word):
        last_guess: GuessScore = self.data.scores[-1]
        dist_from_secret = last_guess.score
        dist_from_guess = self.data.get_distance_of_word(last_guess.word, word)
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

    def e_w_s(self, w, s):
        if not s:
            raise ValueError("State (s) cannot be an empty list")
        # creating array for using numpy.
        s_array = np.array(s)
        words_list = s_array[:, 0]
        distances_lists = s_array[:, 1].astype(float)

        # Use a list comprehension instead of a for loop and append
        dists = [self.data.get_distance_of_word(w, word_prime) for word_prime in words_list]

        # Convert the results list to an array for numpy.
        distances_w_word_primes = np.array(dists)

        # Compute the total sum using numpy.
        total_sum = np.sum((distances_w_word_primes - distances_lists) ** 2)
        return (1 / len(s)) * np.sqrt(total_sum)

    def f_w_s(self, w, s):
        return np.exp(-self.e_w_s(w, s))

    def norm_factor(self, s):
        # converting to array for numpy.
        s_array = np.array(s)
        words = s_array[:, 0]
        # summing f_w_s for each word for the factor.s
        return np.sum(np.exp(-np.array([self.e_w_s(word, s) for word in words])))

    def p_w_s(self, w, s):
        norm_factor = self.data.get_state_norm(s)
        if norm_factor == -1:
            norm_factor = self.norm_factor(s)
            self.data.add_state_norm(s, norm_factor)
        return self.f_w_s(w, s) / norm_factor

    def s_w_w(self, s, w, w_t):
        # adding new tuple of word-dist to the state.
        s_prime = [(word, dist) for word, dist in s if word != w]
        d_w_w_prime = self.data.get_distance_of_word(w, w_t)
        s_prime.append((w, d_w_w_prime))
        return s_prime

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

    def E(self, s):
        entropy = self.data.get_state_norm(s)
        if entropy == -1:
            entropy = self.calc_entropy(s)
            self.data.add_state_entropy(s, entropy)

        return entropy

    def calc_entropy(self, s):
        if not s:
            raise ValueError("State (s) cannot be an empty list")
        # converting to array for numpy.
        s_array = np.array(s)
        words = s_array[:, 0]
        # calculating the probability.
        p_w_s_values = np.array([self.p_w_s(word, s) for word in words])
        Entropy = -np.sum(p_w_s_values * np.log2(p_w_s_values))
        # returning the entropy.
        return Entropy

    def E_s_w(self, s, w):
        # removing w from the words in the state.
        V_s = {word for word, _ in s}
        V_s_without_w = V_s - {w}
        entropy_sum = 0
        # for each word in the remain list, calculate:
        for word in V_s_without_w:
            # call the prob. modify the state with the new word
            p_w_prime_s = self.p_w_s(word, s)
            s_w_w_prime = self.s_w_w(s, w, word)
            # using the original entropy formula for calculation.
            entropy_sum += p_w_prime_s * self.E(s_w_w_prime)
            # returning the E_s_W value for the difference calculation in voi.
        return entropy_sum

    def voi(self, s, item):
        # calculating the new weight to be the difference between E(s) to E(s,w) and updating the weight on the list.
        voi_val = self.E(s) - self.E_s_w(s, item.word)
        # remove the current item from the sorted list
        self.data.words_heap.remove(item)

        # update the weight of the item
        item.weight = abs(voi_val)

        # insert the item back into the sorted list with its new weight
        self.data.words_heap.add(item)

    def calculate_new_weight(self, weight, val):
        if self.vector_value_method == NORM2:
            return self.norm_i(2, weight, val)
        elif self.vector_value_method == NORM1:
            return self.norm_i(1, weight, val)

    def old_calculation(self, item, val):

        # remove the current item from the sorted list
        self.data.words_heap.remove(item)

        # update the weight of the item
        new_weight = self.calculate_new_weight(item.weight, val)
        item.weight = new_weight

        # insert the item back into the sorted list with its new weight
        self.data.words_heap.add(item)

    def new_calculation(self, item):

        if self.vector_value_method == PROB:
            self.prob(item)
        elif self.vector_value_method == VOI:
            self.voi(self.data.state.lis, item)

    def prob(self, item):
        # remove the current item from the sorted list
        self.data.words_heap.remove(item)

        # update the weight of the item
        new_weight = self.p_w_s(item.word, self.data.state.lis)
        item.weight = new_weight

        # insert the item back into the sorted list with its new weight
        self.data.words_heap.add(item)

    def choose_next(self, word_heap):
        # sanity check
        if len(word_heap) == 0:
            raise ValueError("error occurred, there are no words left to guess.")
        if self.error_calc_method == PROB:
            probability = random.random()
            sum = 0
            word_index = 0
            while word_index < len(word_heap) - 1:
                if word_heap[word_index] + sum <= probability:
                    word_index += 1
                    sum += word_heap[word_index]
                else:
                    break
            next_word = word_heap[word_index]
            word_heap.remove(next_word)
            return next_word.word
        else:
            # return the queue top.
            if self.error_calc_method != BRUTE_FORCE:
                next_word = word_heap.pop(0)
            else:
                next_word = random.choice(word_heap)
                word_heap.remove(next_word)

            return next_word.word

    def calculate(self):

        # Modify the items in the queue
        for item in self.data.words_heap:

            if not self.using_entropy:

                # calc new val to add the vector.
                val = self.calculate_new_error_val(item.word)

                # updating the error vector in the queue, and update the weight.
                item.error_vec.append(val)

                # editing the weight
                self.old_calculation(item, val)

            else:
                # in case of the new improved methods.
                self.new_calculation(item)

        # choose the next word guess from the updated list.
        return self.choose_next(self.data.words_heap)
