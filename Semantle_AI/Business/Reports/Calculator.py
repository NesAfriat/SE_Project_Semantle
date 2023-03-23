from collections import OrderedDict


class Calculator:

    def __init__(self):
        self.results = OrderedDict()
        self.run_number = 1

    def add_result(self, num_of_guess, remain_words):
        if num_of_guess in self.results:
            self.results[num_of_guess].append(remain_words)
        else:
            self.results[num_of_guess] = list()
            self.results[num_of_guess].append(remain_words)


    def add_noise_result(self, num_of_guess):
        if num_of_guess in self.results:
            self.results[num_of_guess] += 1
        else:
            self.results[num_of_guess] = 0
            self.results[num_of_guess] += 1

    def add_error_result(self, max_val):
        self.results[self.run_number] = max_val
        self.run_number += 1


    def calc_avg(self):
        ret = OrderedDict()
        for key in self.results.keys():
            # iterate over each pair and sum the result
            guesses_sum = 0
            length = len(self.results[key])
            for res in self.results[key]:
                guesses_sum = guesses_sum + res
            ret[key] = round(guesses_sum / length)
        return ret

    def get_highest_nonzero_key(self, od: OrderedDict) -> str:
        """
        Takes an OrderedDict and returns the highest key in the dictionary that has
        a non-zero value.
        """
        for key in reversed(od.keys()):
            if od[key] != 0:
                return key
        raise ValueError("All values in the dictionary are zero")


