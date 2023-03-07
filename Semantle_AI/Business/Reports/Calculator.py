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


    def get_highest_nonzero_key(self, od: OrderedDict) -> str:
        """
        Takes an OrderedDict and returns the highest key in the dictionary that has
        a non-zero value.
        """
        for key in reversed(od.keys()):
            if od[key] != 0:
                return key
        raise ValueError("All values in the dictionary are zero")