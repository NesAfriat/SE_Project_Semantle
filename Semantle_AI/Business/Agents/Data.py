from copy import copy
from collections import OrderedDict
from sortedcontainers import SortedList


class Data:
    def __init__(self):
        self.words_heap = SortedList([])
        self.guesses = dict()
        self.scores = []
        self.model = None
        self.remain_words = None
        self.last_score = -1
        self.last_word = None
        self.statistics = OrderedDict()
        self.copy_vocab = None
        self.is_priority = False
        self.state = State()

    def add_to_dict(self, word, distance):
        if word not in self.guesses.keys():
            self.last_score = distance
            self.last_word = word
            self.guesses[word] = (distance, self.model.get_word_vec(word))
            self.scores.append(GuessScore(word, distance))

    def setError(self, err):
        self.model.setError(err)

    def set_Priority(self, value):
        self.is_priority = value

    def set_model(self, model):
        self.model = model
        self.remain_words = copy(self.model.get_vocab())
        # initialize the max heap. All weights are 0.
        self.words_heap = SortedList([MyItem(word, 0) for word in self.remain_words])
        self.copy_vocab = copy(self.remain_words)

    def set_model_and_vocab(self, model):
        self.model = model
        self.remain_words = copy(self.model.get_vocab())
        # initialize the max heap. All weights are 0.
        self.words_heap = SortedList([MyItem(word, 0) for word in self.remain_words])
        self.copy_vocab = copy(self.remain_words)

    def get_most_similar(self, vec):
        return self.model.get_most_similar_by_vec(vec)

    def get_word_vec(self, w):
        return self.model.get_word_vec(w)

    def get_guesses(self):
        return self.guesses

    def get_distances(self):
        return [x for x, y in self.guesses.values()]

    def get_distance_of_word(self, last_guess_word, word):

        return self.model.get_distance_of_word(last_guess_word, word)

    def get_points(self):
        return [y for x, y in self.guesses.values()]

    def get_words(self):
        return self.guesses.keys()

    def execute_data(self):
        pass

    def reset(self):
        self.guesses = dict()
        self.scores = []
        self.statistics = OrderedDict()
        self.last_score = -1
        self.last_word = None
        self.state.reset()

    def reset_vocab(self):
        self.remain_words = copy(self.copy_vocab)
        # init the max heap. All weights are 0.
        self.words_heap = SortedList([MyItem(word, 0) for word in self.remain_words])

    def get_statistics(self):
        return self.statistics

    def update_statistic(self):
        # Get last key
        if len(self.statistics) == 0:
            next_pos = 0
        else:
            next_pos = next(reversed(self.statistics)) + 1
        if self.is_priority:
            self.statistics[next_pos] = len(self.words_heap)
        else:
            self.statistics[next_pos] = len(self.remain_words)


# class made for the heap compare function that doesn't know how to compare tuple.
class MyItem:
    def __init__(self, word: str, weight: int):
        self.word = word
        self.error_vec = []
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight or (self.weight == other.weight and self.word < other.word)

    def __repr__(self):
        return f'{self.word} ({self.weight})'

    def __eq__(self, other):
        if isinstance(other, MyItem):
            return self.word == other.word and self.weight == other.weight
        return False


class State:
    def __init__(self):
        self.lis = list()
        self.sum_till_now = 0

    def reset(self):
        self.lis = list()
        self.sum_till_now = 0

    def append(self, word, dist):
        self.lis.append((word, dist))


class GuessScore:
    def __init__(self, word, score):
        self.word = word
        self.score = score
