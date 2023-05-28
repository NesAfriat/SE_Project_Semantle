import random

import numpy as np
from Semantle_AI.Business.Container.GuessScore import GuessScore
from Semantle_AI.Business.Container.MyItem import MyItem
from Semantle_AI.Business.Algorithms.Algorithm import Algorithm
import torch
from Semantle_AI.Business.Container.SortedList import SortedList
from Semantle_AI.Business.Container.State import State
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

    def e_w_s(self, w, s: State, isProb=False):
        if not s:
            raise ValueError("State (s) cannot be an empty list")
        # getting the new value in the state
        if not isProb:
            last_elem = s.lis[-1]
            word = last_elem[0]
            distance = last_elem[1]
            # calculating its distance
            dist = self.data.get_distance_of_word(w, word)
            # add it to the sum
            add_on = (dist - distance) ** 2
        else:
            add_on = 0
        old_sum = s.words_new_sum[w]
        return (1 / len(s.lis)) * np.sqrt(old_sum + add_on)

    def f_w_s(self, w, s: State, isProb=False):
        return np.exp(-self.e_w_s(w, s, isProb))

    def norm_factor(self, s: State, isProb=False):
        # converting to array for numpy.
        s_array = np.array(s.lis)
        words = s_array[:, 0]
        # summing f_w_s for each word for the factor.s
        return np.sum(np.exp(-np.array([self.e_w_s(word, s, isProb) for word in words])))

    def p_w_s(self, w, s: State, isProb=False):
        norm_factor = self.data.get_state_norm(s)
        if norm_factor == -1:
            norm_factor = self.norm_factor(s, isProb)
            self.data.add_state_norm(s, norm_factor)
        return self.f_w_s(w, s, isProb) / norm_factor

    def s_w_w(self, s: State, w, w_t):
        # adding new tuple of word-dist to the state.
        new_state = State()
        new_state.lis = [(word, dist) for word, dist in s.lis if word != w]
        new_state.words_new_sum = s.words_new_sum
        d_w_w = self.data.get_distance_of_word(w, w_t)
        new_state.lis.append((w, d_w_w))
        return new_state

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

    def E(self, s: State):
        entropy = self.data.get_state_entropy(s)
        if entropy == -1:
            entropy = self.calc_entropy(s)
            self.data.add_state_entropy(s, entropy)

        return entropy

    def calc_entropy(self, s: State):
        if not s.lis:
            raise ValueError("State (s) cannot be an empty list")
        # converting to array for numpy.
        s_array = np.array(s.lis)
        words = s_array[:, 0]
        # calculating the probability.
        p_w_s_values = np.array([self.p_w_s(word, s) for word in words])
        Entropy = -np.sum(p_w_s_values * np.log2(p_w_s_values))
        # returning the entropy.
        return Entropy

    def E_s_w(self, s: State, w):
        # removing w from the words in the state.
        V_s = {word for word, _ in s.lis}
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
            del s_w_w_prime
        return entropy_sum

    def voi(self, s: State, item: MyItem):
        # calculating the new weight to be the difference between E(s) to E(s,w) and updating the weight on the list.
        voi_val = self.E(s) - self.E_s_w(s, item.word)

        # update the weight of the item
        self.data.words_heap.change_weight(item=item, value=abs(voi_val))

    def calculate_new_weight(self, weight, val):
        if self.vector_value_method == NORM2:
            return self.norm_i(2, weight, val)
        elif self.vector_value_method == NORM1:
            return self.norm_i(1, weight, val)

    def old_calculation(self, item: MyItem, val):

        # update the weight of the item
        new_weight = self.calculate_new_weight(item.weight, val)
        self.data.words_heap.change_weight(item=item, value=new_weight)

    def new_calculation(self, item):

        if self.vector_value_method == PROB:
            self.prob(item)
        elif self.vector_value_method == VOI:
            self.voi(self.data.state, item)

    def prob(self, item):

        # update the weight of the item
        new_weight = self.p_w_s(item.word, self.data.state, isProb=True)
        self.data.words_heap.change_weight(item=item, value=new_weight)

    def choose_next(self, word_heap: SortedList):
        # sanity check
        if len(word_heap) == 0:
            raise ValueError("error occurred, there are no words left to guess.")
        if self.vector_value_method == PROB:
            probability = random.random()
            sum = 0
            word_index = 0
            while word_index < len(word_heap) - 1:
                item = word_heap.get_by_index(word_index)
                if item.weight + sum <= probability:
                    word_index += 1
                    sum += item.weight
                else:
                    next_word = word_heap.remove(item)
                    return next_word.word
            item = word_heap.get_last_item()
            return item.word
        else:
            # return the queue top.
            if self.error_calc_method != BRUTE_FORCE:
                next_word = word_heap.get_by_index(0)
                word_heap.remove(next_word)
            else:

                next_word = word_heap.pick_random()
            return next_word.word

    def calculate(self):

        # Modify the items in the queue
        for item in self.data.words_heap:

            if not self.using_entropy:

                # calc new val to add the vector.
                val = self.calculate_new_error_val(item.word)

                # editing the weight
                self.old_calculation(item, val)

            else:
                # in case of the new improved methods.
                self.new_calculation(item)

        self.data.words_heap.sort()
        # choose the next word guess from the updated list.
        return self.choose_next(self.data.words_heap)
