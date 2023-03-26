from concurrent.futures import ThreadPoolExecutor, Executor
from Business.Algorithms.Algorithm import Algorithm
import numpy as np

SUM = "SUM"
SUM_RELATIVE = "Sum_Relative"
MSE = "MSE"
BRUTE_FORCE = "Brute_force"
SUM_VEC = "Sum_vec"


class SmartMultiLateration(Algorithm):
    def __init__(self, dist_formula, vec_calc_method=SUM, vec_value_method=MSE):
        super().__init__()
        self.dist_formula = dist_formula
        self.error_calculation_forms = dict([(SUM, self.sum), (SUM_RELATIVE, self.sum_relative),
                                             (BRUTE_FORCE, self.ret_zero())])
        self.vector_value_forms = dict([(MSE, self.mse), (SUM_VEC, self.sum_vec)])
        self.error_calc_method = vec_calc_method
        self.vector_value_method = vec_value_method

    def set_error_method(self, method_name):
        self.error_calc_method = method_name

    def set_vector_calculation_method(self, method_name):
        self.vector_value_method = method_name

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
        former_words = self.data.scores
        dist_from_secret = np.array(list(former_words.values()))
        dist_from_guess = np.array([self.data.model.get_distance_of_word(item, word) for item in former_words])
        ret_vector = dist_from_secret - dist_from_guess
        return ret_vector.tolist()

    def ret_zero(self):
        return 0

    @staticmethod
    def mse_relative(d, s):
        s = np.array(s)
        d = np.array(d)
        nonzero_indices = np.nonzero(s)
        mse = np.mean(((s[nonzero_indices] - d[nonzero_indices]) / s[nonzero_indices]) ** 2)
        return np.sqrt(mse)


    def mse(self, vector):
        # iterate over eac former guess and calculate the mse.
        vector = np.array(vector)
        return np.sqrt(np.sum(np.square(vector)))

    def sum_vec(self, vector):
        # iterate over eac former guess and calculate the mse.
        vector = np.array(vector)
        return np.sum(vector)

    def calculate_error_val(self, word):
        return self.error_calculation_forms[self.error_calc_method](word)

    def calculate_vector_size(self, vector):
        return self.vector_value_forms[self.vector_value_method](vector)

    def calculate(self):

        # Get the items from the priority queue
        items = []

        # Calculate the error vectors and vector values in parallel
        with ThreadPoolExecutor() as executor:
            error_vectors = list(executor.map(self.calculate_error_val, [item.word for item in items]))
            vector_values = list(executor.map(self.calculate_vector_size, error_vectors))

        # Modify the items in the queue with the new weight values
        for i, item in enumerate(items):
            item.weight = vector_values[i]
            items[i] = item

        # Push the modified items back into the priority queue
        for item in items:
            self.data.words_heap.put(item)

        # Return the word with the highest weight
        next_word = self.data.words_heap.get()
        if self.data.words_heap.empty():
            raise ValueError("Error occurred, there are no words left to guess.")
        return next_word.word

        # # code before optimization
        #
        # while not self.data.words_heap.empty():
        #     item = self.data.words_heap.get()
        #     items.append(item)
        #
        # # Modify the items in the queue
        # for i, item in enumerate(items):
        #
        #     # create the error vector
        #     error_vector = self.calculate_error_val(item.word)
        #
        #     # calculating the vector value
        #     dec_val = self.calculate_vector_size(error_vector)
        #
        #     # updating the weight in the queue
        #     items[i] = MyItem(item.word, dec_val)
        #
        # # Push the modified items back into the priority queue
        # for item in items:
        #     self.data.words_heap.put(item)
        #
        # # return the queue top.
        # next_word = self.data.words_heap.get()
        # if self.data.words_heap.empty():
        #     raise ValueError("error occurred, there are no words left to guess.")
        # return next_word.word
