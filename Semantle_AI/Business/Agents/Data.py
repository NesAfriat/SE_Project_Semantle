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
        self.normCache = OrderedDict()
        self.entropyCache = OrderedDict()

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
        self.normCache = dict()

    def add_state_norm(self, state_lis, norm):
        key = f"{len(state_lis)}_{state_lis[-1][0] if state_lis else ''}"  # creates a string key like '3_word'
        self.normCache[key] = norm  # Add the state to the dictionary
        self.update_state_norm()  # Check and remove states that don't meet the criteria

    def add_state_entropy(self, state_lis, entropy):
        key = f"{len(state_lis)}_{state_lis[-1][0] if state_lis else ''}"  # creates a string key like '3_word'
        self.entropyCache[key] = entropy  # Add the state to the dictionary
        self.update_state_entropy()  # Check and remove states that don't meet the criteria

    def update_state_norm(self):
        current_length = None
        # Process keys
        for key in list(self.normCache.keys()):
            length, _ = key.split('_')  # Split the key into length and last word
            length = int(length)  # Convert length to integer
            if current_length is None:
                current_length = length
            if length < current_length - 2 or length > current_length:
                del self.normCache[key]  # Remove this state
            else:
                return

    def update_state_entropy(self):
        current_length = None
        # Process keys
        for key in list(self.entropyCache.keys()):
            length, _ = key.split('_')  # Split the key into length and last word
            length = int(length)  # Convert length to integer
            if current_length is None:
                current_length = length
            if length < current_length - 2 or length > current_length:
                del self.entropyCache[key]  # Remove this state
            else:
                return

    def get_state_norm(self, state_lis):
        key = f"{len(state_lis)}_{state_lis[-1][0] if state_lis else ''}"  # creates a string key like '3_word'
        if key in self.normCache:
            return self.normCache.get(key)
        else:
            return -1

    def get_state_entropy(self, state_lis):
        key = f"{len(state_lis)}_{state_lis[-1][0] if state_lis else ''}"  # creates a string key like '3_word'
        if key in self.entropyCache:
            return self.entropyCache.get(key)
        else:
            return -1

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
        self.normCache = dict()

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

    def __eq__(self, other):
        if isinstance(other, State):
            return self.lis == other.lis and self.sum_till_now == other.sum_till_now
        return False

    def __hash__(self):
        return hash(tuple(self.lis)) ^ hash(self.sum_till_now)


class GuessScore:
    def __init__(self, word, score):
        self.word = word
        self.score = score
