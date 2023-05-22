from collections import OrderedDict


class Calculator:

    def __init__(self):
        self.results = OrderedDict()
        self.run_number = 1

    def add_result(self, num_of_guess, remain_words):
        if num_of_guess in self.results:
            self.results[num_of_guess].update(remain_words)
        else:
            self.results[num_of_guess] = list()
            self.results[num_of_guess].update(remain_words)

    def add_noise_result(self, noise, num_of_guess, word):
        if noise not in self.results:
            self.results[noise] = OrderedDict()

        self.results[noise][word] = num_of_guess

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
