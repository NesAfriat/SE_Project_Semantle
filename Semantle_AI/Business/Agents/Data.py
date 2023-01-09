from copy import copy
from collections import OrderedDict


class Data:
    def __init__(self):
        self.guesses = dict()
        self.model = None
        self.remain_words = None
        self.last_score = -1
        self.last_word = None
        self.statistics = OrderedDict()
        self.copy_vocab = None

    def add_to_dict(self, word, distance):
        if word not in self.guesses:
            self.last_score = distance
            self.last_word = word
            self.guesses[word] = (distance, self.model.get_word_vec(word))

    def set_model(self, model):
        self.model = model
        self.remain_words = copy(self.model.get_vocab())
        self.copy_vocab = copy(self.remain_words)

    def get_most_similar(self, vec):
        return self.model.get_most_similar_by_vec(vec)

    def get_word_vec(self, w):
        return self.model.get_word_vec(w)

    def get_guesses(self):
        return self.guesses

    def get_distances(self):
        return [x for x, y in self.guesses.values()]

    def get_points(self):
        return [y for x, y in self.guesses.values()]

    def get_words(self):
        return self.guesses.keys()

    def execute_data(self):
        pass

    def reset(self):
        self.guesses = dict()
        self.statistics = OrderedDict()
        self.last_score = None
        self.last_word = None

    def reset_vocab(self):
        self.remain_words = copy(self.copy_vocab)

    def get_statistics(self):
        return self.statistics

    def update_statistic(self):
        # Get last key
        if len(self.statistics) == 0:
            next_pos = 0
        else:
            next_pos = next(reversed(self.statistics)) + 1
        self.statistics[next_pos] = len(self.remain_words)
