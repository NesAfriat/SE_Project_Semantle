from Business.Agents.Data import MyItem, GuessScore
from Business.Algorithms.Algorithm import Algorithm
import torch

SUM = "SUM"
SUM_RELATIVE = "Sum_Relative"
MSE = "MSE"
SUM_VEC = "Sum vec"
BRUTE_FORCE = "Brute_force"


class SmartMultiLateration(Algorithm):
    def __init__(self, dist_formula, vec_calc_method=SUM, vec_value_method=MSE):
        super().__init__()
        self.dist_formula = dist_formula
        self.error_calculation_forms = dict([(SUM, self.sum), (SUM_RELATIVE, self.sum_relative)])
        self.vector_value_forms = dict([(MSE, self.mse), (SUM_VEC, self.sum_vec)])
        self.error_calc_method = vec_calc_method
        self.vector_value_method = vec_value_method
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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
        mse = torch.mean(tensor ** 2)
        return torch.sqrt(mse)

    def sum_vec(self, vector):
        tensor_vector = torch.tensor(vector, dtype=torch.float32, device=self.device)
        return torch.sum(tensor_vector).item()

    def ret_zero(self, word):
        return 0

    def calculate_new_error_val(self, word):
        if self.error_calc_method == SUM:
            return self.sum(word)
        elif self.error_calc_method == SUM_RELATIVE:
            return self.sum_relative(word)
        else:
            return self.ret_zero(word)

    def calculate_new_vector_size(self, vector):
        if self.vector_value_method == MSE:
            return self.mse(vector)
        elif self.vector_value_method == SUM_VEC:
            return self.sum_vec(vector)

    def calculate(self):
        # Get the items from the priority queue
        items = []
        while not self.data.words_heap.empty():
            item = self.data.words_heap.get()
            items.append(item)

        # Modify the items in the queue
        for i, item in enumerate(items):
            # calc new val to add the vector.
            val = self.calculate_new_error_val(item.word)

            # updating the error vector in the queue, and update the weight.
            items[i].error_vec.append(val)
            items[i].weight = self.calculate_new_vector_size(items[i].error_vec)

        # Push the modified items back into the priority queue
        for item in items:
            self.data.words_heap.put(item)

        # return the queue top.
        next_word = self.data.words_heap.get()
        if self.data.words_heap.empty():
            raise ValueError("error occurred, there are no words left to guess.")
        return next_word.word
