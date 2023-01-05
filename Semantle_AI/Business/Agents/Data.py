from copy import copy


class Data:
    def __init__(self):
        self.guesses = dict()
        self.model = None
        self.remain_words = None
        self.last_score = None
        self.last_word = None
        self.statistics = dict()

    def add_to_dict(self, word, distance, point):
        if word not in self.guesses:
            self.last_score = distance
            self.last_word = word
            self.guesses[word] = (distance, point)

    def set_model(self, model):
        self.model = model
        self.remain_words = copy(self.model.get_vocab())

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
        self.last_score = None
        self.last_word = None

    def reset_vocab(self, vocabulary):
        self.remain_words = copy(vocabulary)

    def get_statistics(self):
        return self.statistics
