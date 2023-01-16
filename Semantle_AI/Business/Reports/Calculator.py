from collections import OrderedDict


class Calculator:

    def __init__(self, num):
        self.results = OrderedDict()
        self.num_of_runs = num

    def add_result(self, num_of_guess, remain_words):
        if num_of_guess in self.results:
            self.results[num_of_guess].append(remain_words)
        else:
            self.results[num_of_guess] = list()
            self.results[num_of_guess].append(remain_words)

    def calc(self):
        ret = OrderedDict()
        for key in self.results.keys():
            # iterate over each pair and sum the result
            sum = 0
            length = len(self.results[key])
            for res in self.results[key]:
                sum = sum + res
            ret[key] = round(sum / length)
        return ret


