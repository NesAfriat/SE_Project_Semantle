from Business.Algorithms.Algorithm import Algorithm
from Business.Agents.Data import MyItem
import numpy as np
import math

SUM = "SUM"
SUM_RELATIVE = "Sum_Relative"
MSE = "MSE"
SUM_VEC = "Sum vec"


class SmartMultiLateration(Algorithm):
    def __init__(self, dist_formula, vec_calc_method=SUM, vec_value_method=MSE):
        super().__init__()
        self.dist_formula = dist_formula
        self.error_calculation_forms = dict([(SUM, self.sum), (SUM_RELATIVE, self.sum_relative)])
        self.vector_value_forms = dict([(MSE, self.mse), (SUM_VEC, self.sum_vec)])
        self.error_calc_method = vec_calc_method
        self.vector_value_method = vec_value_method

    def set_error_method(self, method_name):
        self.error_calc_method = method_name

    def set_vector_calculation_method(self, method_name):
        self.vector_value_method =method_name

    @staticmethod
    def in_range(distance1, distance2, percentage_error):
        """
        Returns True if the percentage difference between distance1 and distance2 is within percentage_error,
        False otherwise.
        """
        percentage_difference = abs((distance1 - distance2) / distance2) * 100
        return percentage_difference <= percentage_error

    def sum_relative(self, word):
        ret_vector = []
        former_words = self.data.scores
        for item, s in former_words.items():
            dist_from_secret = s
            dist_from_guess = self.data.model.get_distance_of_word(word, item)
            ret_vector.append((dist_from_secret-dist_from_guess)/dist_from_secret)
        return ret_vector

    def sum(self, word):
        ret_vector = []
        former_words = self.data.scores
        for item, s in former_words.items():
            dist_from_secret = s
            dist_from_guess = self.data.model.get_distance_of_word(item, word)
            ret_vector.append(dist_from_secret-dist_from_guess)
        return ret_vector

    def ret_zero(self):
        return 0

    @staticmethod
    def mse_relative(d, s):
        ans = sum([((xi - yi) / xi) ** 2 for xi, yi in zip(s, d)])
        return math.sqrt(ans)

    def mse(self, vector):
        # iterate over eac former guess and calculate the mse.
        dists_sum = 0
        for value in vector:
            dists_sum += math.pow(value, 2)
        return math.sqrt(dists_sum)

    def sum_vec(self, vector):
        # iterate over eac former guess and calculate the mse.
        dists_sum = 0
        for value in vector:
            dists_sum += value
        return dists_sum

    def calculate_error_val(self, word):
        return self.error_calculation_forms[self.error_calc_method](word)

    def calculate_vector_size(self, vector):
        return self.vector_value_forms[self.vector_value_method](vector)

    def calculate(self):
        # Get the items from the priority queue
        items = []
        while not self.data.words_heap.empty():
            item = self.data.words_heap.get()
            items.append(item)

        # Modify the items in the queue
        for i, item in enumerate(items):

            # create the error vector
            error_vector = self.calculate_error_val(item.word)

            # calculating the vector value
            dec_val = self.calculate_vector_size(error_vector)

            # updating the weight in the queue
            items[i] = MyItem(item.word, dec_val)

        # Push the modified items back into the priority queue
        for item in items:
            self.data.words_heap.put(item)

        # return the queue top.
        next_word = self.data.words_heap.get()
        if self.data.words_heap.empty():
            raise ValueError("error occurred, there are no words left to guess.")
        return next_word.word
